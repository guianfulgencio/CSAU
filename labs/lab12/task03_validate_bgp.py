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

import requests
import urllib3
from prettytable import PrettyTable

requests.packages.urllib3.disable_warnings()


def submain(args):
    ###
    #   Headers & URLs definitions
    ###
    restconf_headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    def get_bgp_state():
        bgp_url = "https://{host}/restconf/data/{endpoint}".format(
            host=args.host,
            endpoint="{endpoint}:{container}".format(
                endpoint=args.endpoint,
                container=args.container,
            ),
        )

        get_response = requests.get(
            bgp_url,
            auth=(args.username, args.password),
            headers=restconf_headers,
            verify=False,
        )

        if get_response.status_code == 200:
            bgp_state = get_response.json()
        else:
            bgp_state = []

        print("\nGetting BGP oper state with RESTCONF")
        print(
            "\nBGP Oper State: \n{}".format(
                json.dumps(
                    bgp_state, indent=4, sort_keys=True
                )
            )
        )
        print("\nBGP Payload: None for GET operation")
        print("\nURL: {}".format(bgp_url))
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
                "https://github.com/YangModels/yang/blob/master/vendor/cisco/xe/1693/Cisco-IOS-XE-bgp-oper.yang"
            )
        )

        return bgp_state

    def parse_and_report(bgp_state):
        bgp_state = bgp_state.get(
            "{endpoint}:{container}".format(
                endpoint=args.endpoint,
                container=args.container,
            ),
            {},
        )
        bgp_state_table = PrettyTable(
            [
                "Neighbor-id",
                "Up-time",
                "Prefixes",
                "Session state",
                "Connection State",
            ]
        )

        for n in bgp_state["neighbors"]["neighbor"]:
            bgp_state_table.add_row(
                [
                    n["neighbor-id"],
                    n["up-time"],
                    n["installed-prefixes"],
                    n["session-state"],
                    n["connection"]["state"],
                ]
            )

        print(bgp_state_table)

    bgp_state = get_bgp_state()
    parse_and_report(bgp_state=bgp_state)


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
        "-e",
        "--endpoint",
        help="YANG module name: Cisco-IOS-XE-native",
        required=True,
    )
    required_named.add_argument(
        "-c",
        "--container",
        help="YANG container name: native",
        required=True,
    )
    args = parser.parse_args()

    submain(args)


if __name__ == "__main__":
    main()
