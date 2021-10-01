device_ips = [["10.254.0.1","not connected"], ["10.254.0.2","not connected"], ["10.254.0.3", "not connected"]]

print(device_ips)

for ip in device_ips:
    print("\nAttempting to establish connection with {}".format(ip[0]))
    attempt_count = 0
    while attempt_count < 5:
        print("Establishing connection...")
        attempt_count += 1
    print("Connection Established!")
    ip[1]="connected"

print(device_ips)
