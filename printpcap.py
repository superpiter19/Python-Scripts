from pcapy import open_offline
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacket import IP, TCP, UDP, ICMP
import sys


#MAIN
pcap = open_offline(sys.argv[1])
decoder = EthDecoder()
l2=packet.child()

print ("Done")