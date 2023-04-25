#!/usr/bin/env python3

import subprocess
import argparse
import sys


def get_arguments():
    #CLI arguments for script
    parser = argparse.ArgumentParser()
    #Allows either ip subnet or target(s) specification
    parser.add_argument("-t", "--target", dest="target", help="Target IP or IP subnet. Include multiple targets in a comma seperated list")
    parser.add_argument("-s", "--scan_type", dest="scan_type", help="Scan type [0-5]. 0=Paranoid, 1=Sneaky, 2=Polite, 3=Normal, 4=Aggressive, 5=Insane")
    #Add target import from file
    #Allow output to be exported to a file
    options = parser.parse_args()
    #Require at least target list and scan type
    if not options.target:
        parser.error("[-] Please specify an IP/IP subnet, use --help for more info.")
    if not options.scan_type:
        parser.error("[-] Please specify a scan type, use --help for more info.")
    return options

def scan(ip, scan_type):
    #Ingrate nmap through bash
    #allow min 3 different types of scans
    if scan_type <=5 and scan_type >=0:
        #nmap scan
        #Add progress bar at bottom of screen
        #Look into nmap --script options
        subprocess.call(["nmap", "-T" + scan_type, "-sV", "--version-intensity" + scan_type, "-O", ip])
        #return results as a list containing dictionaries
        return scan_results
    else:
        #Print error and exit
        sys.exit(1)

def print_results():
    #Prints results from nmap scan

###Beginning of Operation###use
if __name__ == '__main__':
    import rootchk
    options = get_arguments()
    rootchk.check()
    scan_results = scan(options.ip, options.scan_type)
