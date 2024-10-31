from prettytable import PrettyTable
from scapy.all import ARP, Ether, srp

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

import auxi
from datetime import datetime


class detectHosts:

    def __init__(self, IP, mask):
        self.table = PrettyTable()
        self.networkRange = auxi.cidr(IP, mask)
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

    async def getInformations(self):
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        informations = []
        clients = self.bySubnet()

        #todo verificar se é um roteador só se AnwserSNMPV2 retornar True
        tasks = [self.isRouter(ip) for ip in clients.keys()]
        router_checks = await asyncio.gather(*tasks)

        # @LUIS: cara eu tive que dar uma mexida a mais aqui mal eu.
        # Coloquei Função: como campo, pois um ativo de rede pode ser alem de roteador um
        # firewall, nat, etc. Então acho que seria interessante ter essa informação como uma array de strings dentro de
        # um campo chamado genérico.

        for (ip, mac), router_status in zip(clients.items(), router_checks):
            informations.append({
                "IP": ip,
                "Mac Address": mac,
                "Owner": auxi.ouiExtractor(mac),
                "Tipo": router_status,
            })
        toJson = {"Date": date, "Devices": informations}
        return toJson

    def display_by_subnet(self):
        clients = self.bySubnet()
        self.table.field_names = ["IP Address", "MAC Address"]
        for ip, mac in clients.items():
            self.table.add_row([ip, mac])


    async def isRouter(self, ip):

        community = 'public'
        oid_route_table = '1.3.6.1.2.1.4.21'  # ipRouteTable

        transport_target = await UdpTransportTarget.create((ip, 161))

        snmpEngine = SnmpEngine()

        # Chamar get_cmd corretamente
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            CommunityData(community),
            transport_target,
            ContextData(),
            ObjectType(ObjectIdentity(oid_route_table))
        )

        snmpEngine.close_dispatcher()
        if errorIndication:
            pass

        elif errorStatus:
            pass
        else:
            print(ip)
            return "Router"

        return "Not Router"



    async def AwnserSNMPV2(self, ip):

        # teste 1: verificar se usa um SNMP

        snmpEngine = SnmpEngine()

        # First SNMP request to get system description
        iterator = get_cmd(
            snmpEngine,
            CommunityData("public", mpModel=0),
            await UdpTransportTarget.create((ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        if errorIndication:
            pass

        elif errorStatus:
            pass
        else:
            return True

        return False