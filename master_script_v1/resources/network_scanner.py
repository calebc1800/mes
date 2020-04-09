#!/usr/bin/env python3

#Written by Blackfire

import scapy.all as scapy
import argparse

def get_arguments():
    #Allowing command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP or IP subnet")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an IP/IP subnet, use --help for more info.")
    return options

def scan(ip):
    #Sets the packet type as ARP
    arp_request = scapy.ARP(pdst=ip)
    #Sets packet destination to broadcast MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #Assigns the broadcast destination to the arp packet
    arp_request_broadcast = broadcast/arp_request
    #Sends the arp packet and captures the results in the variable answered_list
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False) [0]
    #Initializes list
    clients_list = []
    for element in answered_list:
        #Puts a dictionary in each index of the list
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    #Returns the list of dictionaries
    return clients_list

def print_result(results_list):
    #Header
    print("IP\t\t\tMAC Address\n" + "-" * 41)
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

###Beginning of Operation###
if __name__ == '__main__':
    import rootchk
    options = get_arguments()
    rootchk.check()
    scan_result = scan(options.target)
    print_result(scan_result)
