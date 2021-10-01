#! /usr/bin/env python






import requests
import json
import argparse
import sys
import os

# from getpass import getpass
from datetime import datetime
import csv

# Check for module dependencies:
not_installed_modules = []

try:
    from requests.auth import HTTPBasicAuth
except ImportError:
    not_installed_modules.append("requests")
try:
    import yaml
except ImportError:
    not_installed_modules.append("PyYAML")
try:
    from builtins import input as builtins_input
except ImportError:
    not_installed_modules.append("future")

try:
    from consolemenu import ConsoleMenu
    from consolemenu.items import FunctionItem
except ImportError:
    not_installed_modules.append("console-menu")
try:
    from prettytable import PrettyTable
except ImportError:
    not_installed_modules.append("prettytable")

if not_installed_modules:
    print("Please install following Python modules:")

    for module in not_installed_modules:
        print("  - {module}".format(module=module))

    sys.exit(1)

requests.packages.urllib3.disable_warnings()

headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json",
}

def get_lldp_data(host, hosts_username, hosts_password):
    auth = (hosts_username, hosts_password)
    url = "https://{host}/restconf/data/Cisco-IOS-XE-lldp-oper:lldp" "-entries/".format(
        host=host
    )
    response = requests.get(url, headers=headers, auth=auth, verify=False)
    result = json.loads(response.text)
    lldp_data = result["Cisco-IOS-XE-lldp-oper:lldp-entries"]["lldp-entry"]
    return lldp_data

def structure_data(args):
    host = args.device
    hosts_username = args.username
    hosts_password = args.password
    devices = {}
    devices[host] = {}
    devices[host]["lldp"] = get_lldp_data(host, hosts_username, hosts_password)

    return devices


def generate_table(args):

    lldp_table_header = PrettyTable(
        ["Hostname", "Local Interface", "Neighbor", "Neighbor Interface"]
    )

    for hostname, details in structure_data(args).items():
        row = [hostname]
        for lldp_data in details["lldp"]:
            neighbor = lldp_data["device-id"]
            local_int = lldp_data["local-interface"]
            neigh_int = lldp_data["connecting-interface"]
            lldp_table_header.add_row([hostname, neighbor, local_int, neigh_int])

    return {"lldp": lldp_table_header.get_string()}


def text_table(args):
    print(generate_table(args)["lldp"])


def main():
    parser = argparse.ArgumentParser(description="Argparse for Training Course.")
    parser.add_argument(
        "-u", "--username", required=True, help="Username to login to device"
    )
    parser.add_argument("-p", "--password", help="Password to login to the device")
    parser.add_argument('-a', '--ask-pass', action='store_true', help='Prompt for password to login to the device')
    parser.add_argument(
        "-d",
        "--device",
        required=True,
        help="IP Address or Hostname of network device to automate",
    )

    args = parser.parse_args()

#    if not args.ask_pass:
#        args.password = input("Enter password: ")
#    else:
#        args.password = getpass("Enter password: ")

    text_table(args)


if __name__ == "__main__":
    main()
