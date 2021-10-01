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
DEFAULT_INTENT_FILE = ''

#######################
import argparse
import json
from collections import OrderedDict

import requests
import urllib3
import yaml

requests.packages.urllib3.disable_warnings()


def submain(args):
    ###
    #   Headers & URLs definitions
    ###
    restconf_headers = {
        'Accept': 'application/yang-data+json',
        'Content-Type': 'application/yang-data+json'
    }

    def get_intent():
        """
        Returns:
        {'bgp': {'neighbors': [{'peer_as': 300, 'address': '192.0.2.2'}, {'peer_as': 400, 'address': '192.0.2.1'}], 'asn': 100}}
        """
        with open(args.intent) as fh:
            yml_file = yaml.load(fh, Loader=yaml.SafeLoader)

        return yml_file

    def bgp_add():
        od = OrderedDict()

        od["id"] = intent['bgp']['neighbors'][args.add]['address']
        od["remote-as"] = int(intent['bgp']['neighbors'][args.add]['peer_as'])

        bgp_payload = {"Cisco-IOS-XE-bgp:neighbor": [od]}

        bgp_url = 'https://{host}/restconf/data/{endpoint}'.format(
            host=args.host,
            endpoint='Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:router=bgp/{bgp_asn}/neighbor'.format(
                bgp_asn=str(intent['bgp']['asn'])
            ))

        patch_response = requests.patch(bgp_url,
                                        auth=(args.username, args.password),
                                        headers=restconf_headers, verify=False,
                                        data=json.dumps(bgp_payload)
                                        )

        print("\nAdding BGP neighbor with RESTCONF")
        print("\nBGP Payload: \n{}".format(
            json.dumps(bgp_payload, indent=4, sort_keys=True)))
        print("\nURL: {}".format(bgp_url))
        print("\nHeaders: \n{}".format(
            json.dumps(restconf_headers, indent=4, sort_keys=True)))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-bgp.yang"))

    def bgp_remove():
        bgp_url = 'https://{host}/restconf/data/{endpoint}'.format(
            host=args.host,
            endpoint='Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:router=bgp/{bgp_asn}/neighbor={remove}'.format(
                bgp_asn=str(intent['bgp']['asn']),
                remove=intent['bgp']['neighbors'][args.remove]['address'],
            ))

        delete_response = requests.delete(bgp_url,
                                          auth=(args.username, args.password),
                                          headers=restconf_headers,
                                          verify=False,
                                          )

        print("\nRemoving BGP neighbor with RESTCONF")
        print("\nBGP Payload: None for DELETE operation")
        print("\nURL: {}".format(bgp_url))
        print("\nHeaders: \n{}".format(
            json.dumps(restconf_headers, indent=4, sort_keys=True)))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-bgp.yang"))

    def bgp_sync():
        od = OrderedDict()

        od["id"] = int(intent['bgp']['asn'])
        od["neighbor"] = []

        bgp_payload = {"Cisco-IOS-XE-bgp:bgp": od}

        for neighbor in intent['bgp']['neighbors']:
            od_n = OrderedDict()
            od_n['id'] = intent['bgp']['neighbors'][neighbor]['address']
            od_n['remote-as'] = int(
                intent['bgp']['neighbors'][neighbor]['peer_as'])

            bgp_payload['Cisco-IOS-XE-bgp:bgp']['neighbor'].append(od_n)

        bgp_url = 'https://{host}/restconf/data/{endpoint}'.format(
            host=args.host,
            endpoint='Cisco-IOS-XE-native:native/Cisco-IOS-XE-native:router=bgp/{bgp_asn}'.format(
                bgp_asn=str(intent['bgp']['asn'])
            ))

        put_response = requests.put(bgp_url,
                                    auth=(args.username, args.password),
                                    headers=restconf_headers, verify=False,
                                    data=json.dumps(bgp_payload)
                                    )

        print("\nSyncing BGP neighbors with RESTCONF")
        print("\nBGP Payload: \n{}".format(
            json.dumps(bgp_payload, indent=4, sort_keys=True)))
        print("\nURL: {}".format(bgp_url))
        print("\nHeaders: \n{}".format(
            json.dumps(restconf_headers, indent=4, sort_keys=True)))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-bgp.yang"))

    intent = get_intent()

    if args.add:
        bgp_add()

    if args.remove:
        bgp_remove()

    if args.sync:
        bgp_sync()


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
    required_named.add_argument('--intent', help='Intent file',
                                default=DEFAULT_INTENT_FILE,
                                required=False if DEFAULT_INTENT_FILE else True)
    required_named.add_argument('--add', help='Add Neighbor',
                                required=False)
    required_named.add_argument('--remove', help='Remove Neighbor',
                                required=False)
    required_named.add_argument('--sync', help='Sync Neighbors',
                                required=False, action='store_const',
                                const=True)

    args = parser.parse_args()

    submain(args)


if __name__ == '__main__':
    main()

