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
import xml.dom.minidom

from ncclient import manager


def submain(args):
    ###
    #   Headers & URLs definitions
    ###

    def print_native_ifoper():
        filter = """
        <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
        <name>GigabitEthernet1</name>
        </interface>
        </interfaces>
        """

        with manager.connect(
            host=args.host,
            port=830,
            username=args.username,
            password=args.password,
            hostkey_verify=False,
            device_params={"name": "csr"},
            look_for_keys=False,
            allow_agent=False,
        ) as m:
            netconf_response = m.get(
                filter=("subtree", filter)
            )

        print(
            "\nGetting interfaces oper state with NETCONF (using Native Model)"
        )
        pretty_xml = xml.dom.minidom.parseString(
            netconf_response.data_xml
        ).toprettyxml(indent=" ")
        print("\nInterfaces: \n{}".format(pretty_xml))
        print("\nFilter: \n{}".format(filter))
        print(
            "\nYANG Model URL: {}\n".format(
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-interfaces-oper.yang"
            )
        )

        # from lxml import etree
        # pretty_xml = etree.tostring(netconf_response.data_ele, pretty_print=True)

    def print_openconfig_ifoper():
        filter = """
        <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
        <name>GigabitEthernet1</name>
        </interface>
        </interfaces>
        """

        with manager.connect(
            host=args.host,
            port=830,
            username=args.username,
            password=args.password,
            hostkey_verify=False,
            device_params={"name": "csr"},
            look_for_keys=False,
            allow_agent=False,
        ) as m:
            netconf_response = m.get(
                filter=("subtree", filter)
            )

        print(
            "\nGetting interfaces oper state with NETCONF (using Openconfig Model)"
        )
        pretty_xml = xml.dom.minidom.parseString(
            netconf_response.data_xml
        ).toprettyxml(indent=" ")
        print("\nInterfaces: \n{}".format(pretty_xml))
        print("\nFilter: \n{}".format(filter))
        print(
            "\nYANG Model URL: {}\n".format(
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/openconfig-interfaces.yang"
            )
        )

        # from lxml import etree
        # pretty_xml = etree.tostring(netconf_response.data_ele, pretty_print=True)

    if args.model == "native":
        print_native_ifoper()
    elif args.model == "openconfig":
        print_openconfig_ifoper()


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
    required_named.add_argument(
        "-m", "--model", help="Yang Model", required=True
    )

    args = parser.parse_args()

    submain(args)


if __name__ == "__main__":
    main()
