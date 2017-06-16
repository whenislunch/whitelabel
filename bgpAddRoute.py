#!/usr/bin/env python

import sys
import time
import random
from netaddr.ip import IPNetwork, IPAddress

import udpclient
from multiprocessing import Process


ipVersion = 'ipv4'
append = 'end'
messages = []

if ipVersion == 'ipv4':
    announce = 'announce route 100.0.0.0/24 next-hop 90.0.0.1'
elif ipVersion == 'ipv6':
    announce = 'announce route 10::/64 next-hop 90::1'

# get amounts of routes from file, this is optional
with open("routes", "r") as f:
    routeCount = int(f.read())
    print 'ROUTE COUNT FROM FILE: ', routeCount


def announceRoutes(n):
    if ipVersion is 'ipv4':
        target = 'announce route 100.0.0.0/24 next-hop 90.0.0.1'
        FIR = 1
        SEC = 0
        THI = 0
        # generate n random ipv4 addresses and create a list
        for i in range(0, n):
            messages.append("announce route " + str(FIR) + "." + str(SEC) +
                            "." + str(THI) + ".0/24" + " next-hop 90.0.0.1")
            THI = THI + 1
            if THI == 254:
                SEC = SEC + 1
                THI = 0
            if SEC == 254:
                FIR = FIR + 1
                SEC = 0
    else:
        target = 'announce route 10::/64 next-hop 90::1'
        # generate n random ipv6 addresses
        for i in range(0, n):
            random.seed(i)
            ip_a = IPAddress('2001::cafe:0') + random.getrandbits(16)
            ip_n = IPNetwork(ip_a)
            messages.append('announce route ' + str(ip_n) + ' 90::1')
    # target at beginning or end of list
    if append == "first":
        messages.inser(0, target)
    else:
        messages.append(target)
    return messages


def addRoute():
    """
    Announce all routes to exaBGP
    """
    # pop pending routes
    messages = announceRoutes(routeCount)
    sys.stderr.write('popping now...\n')
    startPop = time.time()
    while messages:
        message = messages.pop(0)
        sys.stdout.write(message + '\n')
        sys.stdout.flush()
    endPop = time.time() - startPop
    sys.stderr.write('done popping! took: ' + str(endPop) + '\n')

    # make sure the tool keeps running untill interrupted
    while True:
        time.sleep(5)


def udpPing():
    """
    Run imported udp client script
    """
    udpclient.run(routeCount, ipVersion)


# execute announce and ping thread at same time
p1 = Process(target=addRoute)
p1.start()

p2 = Process(target=udpPing)
p2.start()
