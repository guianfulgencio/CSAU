from netmiko import ConnectHandler

inventory = {
    "csr1kv1": {
        "ip_addr": "10.254.0.1",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
    "csr1kv2": {
        "ip_addr": "10.254.0.2",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
    "csr1kv3": {
        "ip_addr": "10.254.0.3",
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_xe",
    },
}

for router, detail in inventory.items():
    device = ConnectHandler(
        host=detail["ip_addr"],
        username=detail["username"],
        password=detail["password"],
        device_type=detail["device_type"],
    )

    print("Connecting to {}".format(router))

    print("Sending SNMP Configurations to {}...".format(router))

    file_path = "./configs/{}.cfg".format(router)
    device.send_config_from_file(file_path)
    print("Commands sent to device...")

    print("Verifying Configuration {}...".format(router))

    snmp_config = device.send_command("show run | include snmp-server")
    print(snmp_config)
    print("Disconnecting from {}...".format(router))
