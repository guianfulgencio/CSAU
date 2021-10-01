#!/usr/bin/env python

#######################
# Global Vars
#
# Those values are for hard coding the environment.
#
# If needed, they can be overwritten by CLI parameters.
# If no CLI parameters are given, below values will be used.
#
DEFAULT_TARGET_HOST = ''
DEFAULT_USERNAME = 'cisco'
DEFAULT_PASSWORD = 'cisco'

#######################

import argparse
import xml.dom.minidom
from collections import defaultdict

import xmltodict
from jinja2 import Template
from ncclient import manager


def main():
    parser = argparse.ArgumentParser()
    required_named = parser.add_argument_group('Required named arguments')
    required_named.add_argument('--host', help='Target Host',
                                required=True if not DEFAULT_TARGET_HOST else False,
                                default=DEFAULT_TARGET_HOST)
    required_named.add_argument('-u', '--username', help='Username',
                                required=False, default=DEFAULT_USERNAME)
    required_named.add_argument('-p', '--password', help='Password',
                                required=False, default=DEFAULT_PASSWORD)

    args = parser.parse_args()

    submain(args)


def submain(args):
    ###
    #   Headers & URLs definitions
    ###

    def get_lldp_neighbors():
        filter = """
        <lldp-entries xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper">
        </lldp-entries>
        """
        with manager.connect(host=args.host,
                             port=830,
                             username=args.username,
                             password=args.password,
                             hostkey_verify=False,
                             device_params={'name': 'csr'},
                             look_for_keys=False,
                             allow_agent=False) as m:
            netconf_response = m.get(filter=('subtree', filter))

        _d = xmltodict.parse(netconf_response.data_xml)

        print("\nGetting LLDP neighbors with NETCONF")
        pretty_xml = xml.dom.minidom.parseString(
            netconf_response.data_xml).toprettyxml(indent=" ")
        print("\nLLDP Neighbors: \n{}".format(pretty_xml))
        print("\nFilter: \n{}".format(filter))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-lldp-oper.yang"))

        return _d['data']['lldp-entries']['lldp-entry']

    def get_interfaces():
        filter = """
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface></interface>
        </native>
        """

        with manager.connect(host=args.host,
                             port=830,
                             username=args.username,
                             password=args.password,
                             hostkey_verify=False,
                             device_params={'name': 'csr'},
                             look_for_keys=False,
                             allow_agent=False) as m:
            netconf_response = m.get_config(source='running', filter=('subtree', filter))

        print("\nGetting interfaces with NETCONF")
        pretty_xml = xml.dom.minidom.parseString(
            netconf_response.data_xml).toprettyxml(indent=" ")
        print("\nInterfaces: \n{}".format(pretty_xml))
        print("\nFilter: \n{}".format(filter))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang"))


    def map_deviceids_to_interfaces(lldp_neighbors):
        """
        Returns (dict): { u'Gi4': [{device-id: 'csr1kv2.cisco.com', 'connecting-interface': ''} , ... ] }
        """
        data = defaultdict(list)

        for e in lldp_neighbors:
            data[e['local-interface']].append({'device-id': e['device-id'],
                                               'connecting-interface': e[
                                                   'connecting-interface']
                                               })

        return data

    def build_interfaces_payload(interface_dict):

        interfaces = []

        for ifname, ifdata in interface_dict.items():
            # Skip if 0 or multiple LLDP neighbors found on an interface
            if len(ifdata) != 1:
                continue

            # Skip if interface name not startswith Gi
            if not ifname.startswith("Gi"):
                continue
            elif ifname.startswith("Gi"):
                if_type = 'GigabitEthernet'
                if_number = str(ifname.replace('Gi', ''))

            if_descr = 'Connects to {device} on {interface} (auto-configured by NETCONF)'.format(
                device=ifdata[0]['device-id'],
                interface=ifdata[0]['connecting-interface'])

            interfaces.append({
                'index': if_number,
                'type': if_type,
                'description': if_descr,
            })

        with open('task01_native_lldp_descriptions.j2') as f:
            interface_template = Template(f.read())

        interfaces_payload = interface_template.render(interfaces=interfaces)

        print("\nInterfaces Payload: \n{}".format(interfaces_payload))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang"))

        return interfaces_payload

    def send_netconf_payload(netconf_payload):
        with manager.connect(host=args.host,
                             port=830,
                             username=args.username,
                             password=args.password,
                             hostkey_verify=False,
                             device_params={'name': 'csr'},
                             look_for_keys=False,
                             allow_agent=False) as m:
            netconf_response = m.edit_config(netconf_payload, target='running')

        print("\nSending interface descriptions with NETCONF")
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces.yang"))


    lldp_neighbors = get_lldp_neighbors()
    router_interfaces = get_interfaces()
    interface_dict = map_deviceids_to_interfaces(lldp_neighbors=lldp_neighbors)
    interfaces_payload = build_interfaces_payload(interface_dict=interface_dict)
    send_netconf_payload(netconf_payload=interfaces_payload)


if __name__ == '__main__':
    main()

