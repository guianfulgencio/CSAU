cisco_lifecycle_data = {
    "cisco-ios": {
        "latest_release": "15.8(3)M",
        "list_of_supported_devices": ["Catalyst 2960", "Catalyst 4500"],
        "list_of_eol_devices": [
            {"model": "Catalyst 2940", "eol_date": "11/6/2015"},
            {"model": "Catalyst 3560", "eol_date": "11/14/2013"},
        ],
    },
    "cisco-nxos": {
        "latest_release": "7.0(3)I7(6)",
        "list_of_supported_devices": ["Nexus 9508", "Nexus 7000"],
        "list_of_eol_devices": [
            {"model": "Nexus 5500", "eol_date": "05/5/2018"},
            {"model": "Nexus 3500", "eol_date": "12/21/2018"},
        ],
    },
}


# Iterate over the dictionary with the for-loop and print all latest releases

for os, data in cisco_lifecycle_data.items():
    print("Latest release for {} is: {}".format(os, data["latest_release"]))
