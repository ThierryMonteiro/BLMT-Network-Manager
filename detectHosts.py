from prettytable import PrettyTable
from scapy.all import ARP, Ether, srp

class detectHosts:
    def __init__(self):
        pass


    def bySubnet(self, networkRange):
        arp = ARP(pdst=networkRange)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        clients = {}
        for sent, received in result:
            clients[received.psrc] = received.hwsrc

        return clients



    def display_by_subnet(self, networkRange):
        clients = self.bySubnet(networkRange)
        table = PrettyTable()
        table.field_names = ["IP Address", "MAC Address"]
        for ip, mac in clients.items():
            table.add_row([ip, mac])
        print(table)

    #todo adicionar o campo que o raniery pediu de se é novo, antigo, etc
