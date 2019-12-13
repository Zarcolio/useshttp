#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from tldextract import extract
import signal
import argparse
import re
import requests

def fHttpTest(sProtocol, sInFqdn, sPort, aStatus):
    sHttpUrl = sProtocol + "://" + sInFqdn + ":" + sPort
    try:
        rHttp = requests.get(sHttpUrl)
        if args.status is None:
            sys.stdout.write (sHttpUrl + "\n")
        else:
            for sStatus in aStatus:
                sStatus = sStatus.lower()
                if re.match(r"^[1-5][0-9][0-9]$", sStatus):
                    if str(rHttp.status_code) == sStatus:
                        sys.stdout.write (sHttpUrl + "\n")
                elif sStatus == "info" or sStatus == "success" or sStatus == "redirect" or sStatus == "client-error" or sStatus == "server-error":
                    #print ("test")
                    iHttpStatus = int(rHttp.status_code)
                    if sStatus == "info" and iHttpStatus >= 100 and iHttpStatus <200:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "success" and iHttpStatus >= 200 and iHttpStatus <300:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "redirect" and iHttpStatus >= 300 and iHttpStatus <400:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "client-error" and iHttpStatus >= 400 and iHttpStatus <500:
                        sys.stdout.write (sHttpUrl + "\n")
                    if sStatus == "server-error" and iHttpStatus >= 500 and iHttpStatus <600:
                        sys.stdout.write (sHttpUrl + "\n")
                else:
                    print ("Invalid HTTP status code(s)")
                    sys.exit()
    except requests.exceptions.RequestException:
        pass

    

def signal_handler(sig, frame):
        print("\nCtrl-C detected, exiting...\n")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

sRegex = r'((?!-)[-A-Z\d]{1,62}(?<!-)\.)+[A-Z]{1,62}'

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--ports", help="List of ports, separated by commas. Don't use spaces.")
parser.add_argument("-s", "--status", help="List of HTTP status codes, separated by commas. Don't use spaces.")
args = parser.parse_args()


if args.ports is None:
    sPortArg = "80,443"
else:
    sPortArg = args.ports

aPorts = sPortArg.split(",")

if args.status is not None:
    aStatus = args.status.split(",")
else:
    aStatus = []

for sInFqdn in sys.stdin:
    sInFqdn = sInFqdn.strip()
    found = re.match(sRegex, sInFqdn,re.IGNORECASE)
    if found:
        for sPort in aPorts:
            fHttpTest("https", sInFqdn, sPort, aStatus)
            fHttpTest("http", sInFqdn, sPort, aStatus)
    else:
        print (sInFqdn + " isn't a valid FQDN")
