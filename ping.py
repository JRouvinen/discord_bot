#ping.py
#!/usr/bin/env python3

import os

def ping_homelab():

    ip_dictionary = {
        "Gateway":"172.31.5.5",
        "PiHole":"172.31.5.35",
        "NUC11_eth":"172.31.5.30",
        "NUC11_wifi": "172.31.5.31",
        "filesrv": "172.31.5.33",
        "jellyfin_eth": "172.31.5.25",
        "jellyfin_wifi": "172.31.5.41",
        "zbook_eth":"172.31.5.26",
        "zbook_wifi": "172.31.5.32",
    }

    ping_results = {}

    for ip in ip_dictionary:
        response = os.popen(f"ping {ip_dictionary[ip]}").read()
        # Pinging each IP address 4 times
        if response.count("unreachable") != 0 or response.count("timed out") != 0:
            #print(f"❌ {ip} Ping Unsuccessful, Host is DOWN.")
            ping_results[ip] = "❌ - DOWN"

        else:
            #print(f"✅ {ip} Ping Successful, Host is UP!")
            ping_results[ip] = "✅ - UP"

    return ping_results


