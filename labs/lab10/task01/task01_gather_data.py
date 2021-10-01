#! /usr/bin/env python

import requests
import json

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


if not_installed_modules:
    print("Please install following Python modules:")

    for module in not_installed_modules:
        print("  - {module}".format(module=module))

    sys.exit(1)



def get_inventory():
    inventory = {
        "csr1kv1": {"username": "cisco", "password": "cisco"},
        "csr1kv2": {"username": "cisco", "password": "cisco"},
    }

    return inventory


def get_hostname(host):
    url = "https://{host}/restconf/data/Cisco-IOS-XE-native:native" "/hostname".format(
        host=host
    )
    response = requests.get(url, headers=HTTP_HEADERS, auth=HTTP_AUTH, verify=False)
    result = json.loads(response.text)
    hostname = result.get("Cisco-IOS-XE-native:hostname")

    return hostname


def structure_data():

    devices = {}
    net_inventory = get_inventory()
    for host in net_inventory:
        devices[host] = {}
        devices[host]["hostname"] = get_hostname(host)
    return devices


def main():

    structured_data = structure_data()

    heading = "| {:^10} | {:^10} |".format(
        "Device", "Hostname"
    )
    print(len(heading) * "-")
    print(heading)
    print(len(heading) * "-")
    for hostname, details in structured_data.items():
        print(
            "| {:^10} | {:^10} |".format(
                hostname,
                details["hostname"]
            )
        )
        print(len(heading) * "-")

if __name__ == "__main__":
    main()
