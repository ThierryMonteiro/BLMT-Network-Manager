from prettytable import PrettyTable
from scapy.all import ARP, Ether, srp
import aux
from datetime import datetime

class detectHosts:

    def __init__(self, IP, mask):
        self.table = PrettyTable()
        self.networkRange = aux.cidr(IP, mask)
        self.display_by_subnet()

    def bySubnet(self):
        arp = ARP(pdst=self.networkRange)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        clients = {}
        for sent, received in result:
            clients[received.psrc] = received.hwsrc

        return clients

    def printTable(self):
        print(self.table)

    def getInformations(self):
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        informations = []
        clients = self.bySubnet()
        for ip, mac in clients.items():
            informations.append({
                "IP": ip,
                "Mac Address": mac,
                "Owner": aux.ouiExtractor(mac)
            })
        toJson = {"Date": date, "Devices": informations}
        return toJson

    def display_by_subnet(self):
        clients = self.bySubnet()
        self.table.field_names = ["IP Address", "MAC Address"]
        for ip, mac in clients.items():
            self.table.add_row([ip, mac])


    #todo adicionar o campo que o raniery pediu de se é novo, antigo, etc
