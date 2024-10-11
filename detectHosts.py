from scapy.all import ARP, Ether, srp

class detectHosts:
    def __init__(self):
        pass


    def bySubrange(self, networkRange):

        #for ip in ipsCalc().ipRange(networkRange):

        arp = ARP(pdst=networkRange)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=3, verbose=0)[0]


        clients = []
        for sent, received in result:
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})

        print("Available devices in the network:")
        print("IP" + " " * 18 + "MAC")
        for client in clients:
            print("{:16}    {}".format(client['ip'], client['mac']))


