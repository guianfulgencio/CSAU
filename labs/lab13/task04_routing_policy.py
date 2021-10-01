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
DEFAULT_INTENT_FILE = None
#######################

import argparse

import yaml
from jinja2 import Template
from ncclient import manager


def submain(args):
    ###
    #   Headers & URLs definitions
    ###
    def get_intent():
        """
        Returns:
        {'bgp': {'neighbors': [{'peer_as': 300, 'address': '192.0.2.2'}, {'peer_as': 400, 'address': '192.0.2.1'}], 'asn': 100}}
        """
        with open(args.intent) as fh:
            yml_file = yaml.load(fh, Loader=yaml.SafeLoader)

        return yml_file

    def build_routing_policy_payload():
        interfaces = intent.get('interfaces', [])

        with open('task04_routing_policy.j2') as f:
            interface_template = Template(f.read())

        _routing_policy_payload = interface_template.render(
            interfaces=interfaces)

        print("\nRouting Policy Payload: \n{}".format(_routing_policy_payload))
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/openconfig-routing-policy.yang"))

        return _routing_policy_payload

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

        print("\nSending routing policy configuration with NETCONF")
        print("\nYANG Model URL: {}\n".format(
            "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/openconfig-routing-policy.yang"))

    intent = get_intent()

    routing_policy_payload = build_routing_policy_payload()
    send_netconf_payload(netconf_payload=routing_policy_payload)


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

    args = parser.parse_args()

    submain(args)


if __name__ == '__main__':
    main()

