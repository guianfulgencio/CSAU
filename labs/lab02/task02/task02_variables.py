inventory = {
    "nycr01": {
        "vendor": "cisco",
        "os_version": 16.8,
        "platform": "csr1kv",
        "os_type": "ios",
        "hostname": "csr1kv1",
    },
    "nxos-spine1": {
        "vendor": "cisco",
        "os_version": 9.0,
        "platform": "nexus",
        "os_type": "nxos",
        "hostname": "nxos-spine1",
    },
}
neighbor_data = {
    "Eth1": [
        {"neighbor": "r1", "neighbor_interface": "Eth1"},
        {"neighbor": "r2", "neighbor_interface": "Eth2"},
    ],
    "Eth2": [
        {"neighbor": "r1", "neighbor_interface": "Eth5"}
    ],
    "Eth3": [
        {"neighbor": "r3", "neighbor_interface": "Eth3"}
    ],
}
