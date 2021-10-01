from netmiko import ConnectHandler
import devnet

config_data = {
    "csr1kv1": {
        "rid": "10.200.10.1",
        "asn": 65512,
        "peers": [
            {"neighbor": "csr1kv2", "ip": "10.12.0.2", "asn": 65513},
            {"neighbor": "csr1kv3", "ip": "10.13.0.3", "asn": 65514},
        ],
    },
    "csr1kv2": {
        "rid": "10.200.10.2",
        "asn": 65513,
        "peers": [
            {"neighbor": "csr1kv1", "ip": "10.12.0.1", "asn": 65512},
            {"neighbor": "csr1kv3", "ip": "10.23.0.3", "asn": 65514},
        ],
    },
    "csr1kv3": {
        "rid": "10.200.10.3",
        "asn": 65514,
        "peers": [
            {"neighbor": "csr1kv1", "ip": "10.13.0.1", "asn": 65512},
            {"neighbor": "csr1kv2", "ip": "10.23.0.2", "asn": 65513},
        ],
    },
}


for router, details in inventory.items():
    print("\nConnecting to {}...".format(router))
    device = ConnectHandler(
        host=router,
        username=details["username"],
        password=details["password"],
        device_type=details["device_type"],
    )
    bgp_commands = []
    bgp_data = config_data[router]
    print("Generating commands for {}...".format(router))
    bgp_commands.append("bgp {}".format(bgp_data["asn"]))
    bgp_commands.append("bgp router-id {}".format(bgp_data["rid"]))
    bgp_neighbor_commands = []
    for bgp_neighbor in bgpdata["peers"]:
        neighbor = "neighbor {} remote-as {}".format(
            bgp_neighbor["ip"], bgp_neighbor["asn"]
        )
        bgp_neighbor_commands.append(neighbor)
    bgp_commands.extend(bgp_neighbor_commands)
    # print("Generated the following commands for {}...".format(router))
    # for command in bgp_commands:
    #    print("    " + command)
    print("Applying the configuration to {}".format(router))
    device.send_config_set(bgp_commands)
    print("\nVerifying if the configuration was successfully applied...")
    show_comand = device.send_command("show run | section bgp")
    print(show_comand)
    device.disconnect()
    print("Disconnecting from {}...".format(router))
    print("#" * 50)
