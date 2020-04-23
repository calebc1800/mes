#!/usr/bin/env python3

import os
import sys

def check():
    if not os.geteuid()==0:
        sys.exit("[-] This script must be run as root!")

