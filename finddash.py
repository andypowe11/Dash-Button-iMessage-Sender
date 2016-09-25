#!/usr/bin/env python

from scapy.all import *

def arp_monitor_callback(pkt):
  if ARP in pkt and pkt[ARP].op == 1: #who-has
    return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

sniff(prn=arp_monitor_callback, filter="arp", store=0)
