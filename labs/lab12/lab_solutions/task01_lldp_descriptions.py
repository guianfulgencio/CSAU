#!/usr/bin/env python

#######################
# Global Vars
#
# Those values are for hard coding the environment.
#
# If needed, they can be overwritten by CLI parameters.
# If no CLI parameters are given, below values will be used.
#
DEFAULT_TARGET_HOST = ""
DEFAULT_USERNAME = "cisco"
DEFAULT_PASSWORD = "cisco"

#######################
import argparse
import json
from collections import defaultdict

import requests
import urllib3

requests.packages.urllib3.disable_warnings()


def main():
    parser = argparse.ArgumentParser() 
    required_named = parser.add_argument_group( 
        "Required named arguments" 
    ) 
    required_named.add_argument( 
        "--host", 
        help="Target Host", 
        required=True if not DEFAULT_TARGET_HOST else False, 
        default=DEFAULT_TARGET_HOST, 
    ) 
    required_named.add_argument( 
        "-u", 
        "--username", 
        help="Username", 
        required=False, 
        default=DEFAULT_USERNAME, 
    ) 
    required_named.add_argument( 
        "-p", 
        "--password", 
        help="Password", 
        required=False, 
        default=DEFAULT_PASSWORD, 
    ) 

    args = parser.parse_args() 

    submain(args) 


def submain(args):
    ### 
    #   Headers & URLs definitions 
    ### 

    restconf_headers = { 
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    } 

    def get_lldp_neighbors(host): 
        lldp_url = "https://{host}/restconf/data/{endpoint}".format( 
            host=host, 
            endpoint="Cisco-IOS-XE-lldp-oper:lldp-entries/", 
        ) 

        get_response = requests.get( 
            lldp_url, 
            auth=(args.username, args.password), 
            headers=restconf_headers, 
            verify=False, 
        ) 

        if get_response.status_code == 200: 
            data = get_response.json() 
            lldp_neighbors = data.get( 
                "Cisco-IOS-XE-lldp-oper:lldp-entries", {} 
            ).get("lldp-entry", []) 
        else: 
            print("Something went wrong") 
            print( 
                "{} returned {} Error Code and following message\n{}".format( 
                    host, 
                    get_response.status_code, 
                    get_response.text, 
                ) 
            ) 
            exit() 

        print("\nGetting LLDP neighbors with RESTCONF") 
        print( 
            "\nLLDP Neighbors: \n{}".format( 
                json.dumps( 
                    lldp_neighbors, indent=4, sort_keys=True 
                ) 
            ) 
        ) 
        print("\nURL: {}".format(lldp_url)) 
        print( 
            "\nHeaders: \n{}".format( 
                json.dumps( 
                    restconf_headers, 
                    indent=4, 
                    sort_keys=True, 
                ) 
            ) 
        ) 
        print( 
            "\nYANG Model URL: {}\n".format( 
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-lldp-oper.yang" 
            ) 
        ) 

        return lldp_neighbors 

    def map_deviceids_to_interfaces(lldp_neighbors): 
        """ 
        Returns (dict): { u'Gi4': [{device-id: 'csr1kv2.cisco.com', 'connecting-interface': ''} , ... ] } 
        """ 
        data = defaultdict(list) 

        for e in lldp_neighbors: 
            data[e["local-interface"]].append( 
                { 
                    "device-id": e["device-id"], 
                    "connecting-interface": e[ 
                        "connecting-interface" 
                    ], 
                } 
            ) 

        return data 

    def build_interfaces_payload(interface_dict): 
        interfaces_payload = { 
            "Cisco-IOS-XE-native:interface": { 
                "GigabitEthernet": [] 
            } 
        } 

        for ifname, ifdata in interface_dict.items(): 
            # Skip if 0 or multiple LLDP neighbors found on an interface 
            if len(ifdata) != 1: 
                continue 

            # Skip if interface name not startswith Gi 
            if not ifname.startswith("Gi"): 
                continue 

            if_number = str(ifname.replace("Gi", "")) 

            interfaces_payload[ 
                "Cisco-IOS-XE-native:interface" 
            ]["GigabitEthernet"].append( 
                { 
                    "name": if_number, 
                    "description": "Connects to {device} on {interface} (auto-configured by RESTCONF)".format( 
                        device=ifdata[0]["device-id"], 
                        interface=ifdata[0][ 
                            "connecting-interface" 
                        ], 
                    ), 
                } 
            ) 

        print( 
            "\nInterfaces Payload: \n{}".format( 
                json.dumps( 
                    interfaces_payload, 
                    indent=4, 
                    sort_keys=True, 
                ) 
            ) 
        ) 
        print( 
            "\nYANG Model URL: {}\n".format( 
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang" 
            ) 
        ) 

        return interfaces_payload 

    def get_interfaces(): 
        """ 
        Function to get interfaces 
        """ 
        interfaces_url = "https://{host}/restconf/data/{endpoint}".format( 
            host=args.host, 
            endpoint="Cisco-IOS-XE-native:native/interface", 
        ) 

        get_response = requests.get( 
            interfaces_url, 
            auth=(args.username, args.password), 
            headers=restconf_headers, 
            verify=False, 
        ) 

        if get_response.status_code == 200: 
            if_data = get_response.json() 

        print("\nGetting interfaces data with RESTCONF") 
        print( 
            "\nInterfaces: \n{}".format( 
                json.dumps( 
                    if_data, indent=4, sort_keys=True 
                ) 
            ) 
        ) 
        print("\nURL: {}".format(interfaces_url)) 
        print( 
            "\nHeaders: \n{}".format( 
                json.dumps( 
                    restconf_headers, 
                    indent=4, 
                    sort_keys=True, 
                ) 
            ) 
        ) 
        print( 
            "\nYANG Model URL: {}\n".format( 
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang" 
            ) 
        ) 

    def patch_interfaces(host, interfaces_payload): 
        """ 
        Function to send a message to update interfaces 
        """ 
        interfaces_url = "https://{host}/restconf/data/{endpoint}".format( 
            host=host, 
            endpoint="Cisco-IOS-XE-native:native/interface", 
        ) 

        patch_response = requests.patch( 
            interfaces_url, 
            auth=(args.username, args.password), 
            headers=restconf_headers, 
            verify=False, 
            data=json.dumps(interfaces_payload), 
        ) 

        print( 
            "\nSending interface description data with RESTCONF" 
        ) 
        print("\nURL: {}".format(interfaces_url)) 
        print( 
            "\nHeaders: \n{}".format( 
                json.dumps( 
                    restconf_headers, 
                    indent=4, 
                    sort_keys=True, 
                ) 
            ) 
        ) 
        print( 
            "\nYANG Model URL: {}\n".format( 
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang" 
            ) 
        ) 

    lldp_neighbors = get_lldp_neighbors(host=args.host) 
    router_interfaces = get_interfaces() 
    interface_dict = map_deviceids_to_interfaces( 
        lldp_neighbors=lldp_neighbors 
    ) 
    interfaces_payload = build_interfaces_payload( 
        interface_dict=interface_dict 
    ) 
    patch_interfaces( 
        host=args.host, 
        interfaces_payload=interfaces_payload, 
    ) 


if __name__ == "__main__":
    main()

