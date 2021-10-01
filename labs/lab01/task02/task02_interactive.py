#!/usr/bin/env python

import argparse
import csv
import json
import os
import sys
from datetime import datetime

# Check for module dependencies:
not_installed_modules = []

try:
    import requests
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

if not os.path.exists("reports"):
    os.mkdir("reports")

DEFAULT_INVENTORY_FILE = "inventory.yml"
DEFAULT_INTENT_FILE = "intent.yml"


def submain(args):
    def get_inventory(inventory):
        with open(inventory) as fh:
            yml_file = yaml.safe_load(fh)

        return yml_file

    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json",
    }

    def get_intent(intent):
        with open(intent) as fh:
            yml_file = yaml.safe_load(fh)

        return yml_file

    def get_lldp_entries(host, username, password):
        url = (
            "https://{host}/restconf/data/Cisco-IOS-XE-lldp-oper:lldp"
            "-entries/".format(host=host)
        )
        response = requests.get(
            url, headers=headers, auth=(username, password), verify=False
        )
        result = json.loads(response.text)
        lldp_entries = result["Cisco-IOS-XE-lldp-oper:lldp-entries"]["lldp-entry"]

        return lldp_entries

    def get_version(host, username, password):
        url = (
            "https://{host}/restconf/data/Cisco-IOS-XE-native:native"
            "/version".format(host=host)
        )
        response = requests.get(
            url, headers=headers, auth=(username, password), verify=False
        )
        result = json.loads(response.text)
        version = result.get("Cisco-IOS-XE-native:version")

        return version

    def get_serial(host, username, password):
        auth = (username, password)
        url = (
            "https://{host}/restconf/data/Cisco-IOS-XE-native:native"
            "/license/udi/sn".format(host=host)
        )
        response = requests.get(url, headers=headers, auth=auth, verify=False)
        result = json.loads(response.text)
        serial_data = result["Cisco-IOS-XE-native:sn"]
        return serial_data

    def get_hostname(host, username, password):
        url = (
            "https://{host}/restconf/data/Cisco-IOS-XE-native:native"
            "/hostname".format(host=host)
        )
        response = requests.get(
            url, headers=headers, auth=(username, password), verify=False
        )
        result = json.loads(response.text)
        hostname = result.get("Cisco-IOS-XE-native:hostname")

        return hostname

    def generate_data():
        devices = {}
        my_inventory = get_inventory(args.inventory)
        for host in my_inventory:
            password = my_inventory[host]["password"]
            username = my_inventory[host]["username"]
            devices[host] = {}
            devices[host]["version"] = get_version(
                host=host, username=username, password=password
            )
            devices[host]["lldp"] = get_lldp_entries(
                host=host, username=username, password=password
            )
            devices[host]["hostname"] = get_hostname(
                host=host, username=username, password=password
            )
            devices[host]["serial"] = get_serial(
                host=host, username=username, password=password
            )
        return devices

    def check_hostname_parameter(existing_state, intented_state):
        if existing_state == intented_state:
            result = "PASS"
        else:
            result = "FAIL"

        return result

    def check_version_parameter(existing_state, intented_state):
        if existing_state in intented_state:
            result = "PASS"
        else:
            result = "FAIL"

        return result

    def check_lldp(existing_state, intented_state):

        if intented_state != len(existing_state):
            result = "FAIL"
        else:
            result = "PASS"

        return result

    def generate_table():

        real_data_from_devices = generate_data()

        table = PrettyTable()
        table.field_names = ["Device", "Hostname", "OS Version", "Neighbors"]

        for host, intended_state in get_intent(args.intent).items():
            version_match = check_version_parameter(
                existing_state=real_data_from_devices[host]["version"],
                intented_state=intended_state["supported_os_versions"],
            )

            hostname_match = check_hostname_parameter(
                existing_state=real_data_from_devices[host]["hostname"],
                intented_state=intended_state["expected_hostname"],
            )

            lldp_match = check_lldp(
                existing_state=real_data_from_devices[host]["lldp"],
                intented_state=intended_state["expected_lldp_neighbors"],
            )

            table.add_row([host, hostname_match, version_match, lldp_match])

        return table.get_string()

    def display_table():
        print("Network Compliance Dashboard\n")
        table = generate_table()
        table += "\n\nPress Enter to Exit to Menu\n"
        user_input = builtins_input(table)
        print(user_input)

    def text_table():

        filename = "./reports/{}.txt".format(
            datetime.now().strftime("{}_%Y_%m_%d_{}_%H_%M_%S".format("Date", "Time"))
        )
        with open(filename, "w") as f:
            f.write(generate_table())
        print("Currently Generating Text Report...")
        print("Filename: {}".format(filename))
        user_input = input("Press Enter to return to continue...")

    def csv_file():

        real_data_from_devices = generate_data()
        filename = "./reports/{}.csv".format(
            datetime.now().strftime("{}_%Y_%m_%d_{}_%H_%M_%S".format("Date", "Time"))
        )
        compliance_file = open(filename, "w")
        with compliance_file:
            header = ["Device", "Hostname", "OS Version", "Neighbors"]
            writer = csv.DictWriter(
                compliance_file,
                fieldnames=header,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL,
                lineterminator="\n\n",
            )
            writer.writeheader()

            for host, intended_state in get_intent(args.intent).items():
                version_match = check_version_parameter(
                    existing_state=real_data_from_devices[host]["version"],
                    intented_state=intended_state["supported_os_versions"],
                )

                hostname_match = check_hostname_parameter(
                    existing_state=real_data_from_devices[host]["hostname"],
                    intented_state=intended_state["expected_hostname"],
                )

                lldp_match = check_lldp(
                    existing_state=real_data_from_devices[host]["lldp"],
                    intented_state=intended_state["expected_lldp_neighbors"],
                )
                writer.writerow(
                    {
                        "Device": host,
                        "Hostname": hostname_match,
                        "OS Version": version_match,
                        "Neighbors": lldp_match,
                    }
                )

        print("Currently Generating CSV Report...")
        print("Filename: {}".format(filename))
        user_input = input("Press Enter to return to continue...")

    def both_reports():
        text_table()
        csv_file()

    def show_lldp_neighbors():
        data = generate_data()

        lldp_table_header = PrettyTable(
            ["Hostname", "Local Interface", "Neighbor", "Neighbor Interface"]
        )

        for hostname, details in data.items():
            row = [hostname]
            for lldp_data in details["lldp"]:
                neighbor = lldp_data["device-id"]
                local_int = lldp_data["local-interface"]
                neigh_int = lldp_data["connecting-interface"]
                lldp_table_header.add_row([hostname, local_int, neighbor, neigh_int])

        print(lldp_table_header.get_string())
        user_input = builtins_input("\nPress Enter to Exit to Menu...\n")

    def show_device_facts():
        data = generate_data()

        main_table = ["OS Version", "Serial Number"]
        main_table_header = PrettyTable()
        main_table.insert(0, "Hostname")

        main_table_header.field_names = main_table
        for hostname, details in data.items():
            row = []
            row.append(details["hostname"])
            row.append(details["version"])
            row.append(details["serial"])
            main_table_header.add_row(row)

        print(main_table_header.get_string())
        user_input = builtins_input("\nPress Enter to Exit to Menu...\n")

    def show_intent_menu():

        menu = ConsoleMenu("Lab 1 - Task 2", "Manage Network Intent")
        menu_items = [
            ("View Compliance Report on Terminal", display_table),
            ("Generate Text Compliance Report", text_table),
            ("Generate CSV Compliance Report", csv_file),
            ("Generate both Reports", both_reports),
        ]
        for item in menu_items:
            menu.append_item(FunctionItem(item[0], item[1]))
        menu.show()

    def show_initial_menu():

        menu = ConsoleMenu("Lab 1 - Task 2", "Console Driven Network Operations")
        menu_items = [
            ("Manage Network Intent", show_intent_menu),
            ("View LLDP Neighbors", show_lldp_neighbors),
            ("View Device Facts", show_device_facts),
        ]
        for item in menu_items:
            menu.append_item(FunctionItem(item[0], item[1]))
        menu.show()

    show_initial_menu()


def main():
    parser = argparse.ArgumentParser(description="Argparse for Training Course.")

    required_named = parser.add_argument_group("Required named arguments")

    required_named.add_argument(
        "--intent",
        help="Intent file",
        default=DEFAULT_INTENT_FILE,
        required=False if DEFAULT_INTENT_FILE else True,
    )
    required_named.add_argument(
        "--inventory",
        help="Inventory File",
        default=DEFAULT_INVENTORY_FILE,
        required=False if DEFAULT_INVENTORY_FILE else True,
    )

    args = parser.parse_args()

    if not os.path.isfile(args.inventory):
        sys.exit("Please specify valid, readable YAML file with data")

    if not os.path.isfile(args.intent):
        sys.exit("Please specify valid, readable intended configuration file with data")

    submain(args)


if __name__ == "__main__":
    main()