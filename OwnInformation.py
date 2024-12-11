import socket
import netifaces as ni
from prettytable import PrettyTable

class managerDevice:
    def __init__(self):
        self.ignoredInterfaces = []
        self.interfaces = self.ips = self.IPdict = None
        self.getInterfacesAndIps()
        self.gateway = self.getGateway()
        self.table = PrettyTable()
        self.table.field_names = ["Interface", "IP Address", "Netmask", "Broadcast"]
        self.formatTable()  # Initialize the table with data

    def formatTable(self):
        """Format the table from the provided data."""
        self.table.clear_rows()  # Clear the table before adding new data
        # Loop through the data and add each row to the table
        for interface, details in self.IPdict.items():
            for detail in details:
                if 'broadcast' not in detail:
                    continue
                self.table.add_row([interface, detail['addr'], detail['netmask'], detail['broadcast']])

    def print_table(self):
        """Print the formatted table."""
        print(self.table)

    def get_table_string(self):
        """Get the formatted table as a string."""
        return str(self.table)

    def getNetworkRange(self):
        mask = []
        for interface in self.interfaces:
            mask.append(ni.ifaddresses(interface)[ni.AF_INET][0]['netmask'])
        return mask

    def getInterfacesAndIps(self) -> None:
        self.interfaces = []
        self.ips = []
        self.IPdict = {}
        lastException = None
        # `netifaces` é uma biblioteca maligna que não integra com a API do módulo `sockets`
        # Não tô com saco pra explicar, mas aqui está a evidência científica:
        # [Links relacionados ao Windows e netifaces]

        for name in ni.interfaces():
            try:
                le_dict = ni.ifaddresses(name)[ni.AF_INET]
                ip = le_dict[0]['addr']
            except TypeError:
                raise
            except Exception as e:
                self.ignoredInterfaces.append(name)
                lastException = e
            else:
                # Verificando se o IP é um IP de loopback (127.0.0.1) e ignorando-o
                if ip.startswith("127."):
                    continue  # Ignora interfaces com IP de loopback (localhost)
                
                self.interfaces.append(name)
                self.ips.append(ip)
                self.IPdict[name] = le_dict

        if len(self.ignoredInterfaces) > 0:
            print("Ignorando " + str(len(self.ignoredInterfaces)) + " interfaces por não terem IP:")
            print(", ".join(self.ignoredInterfaces))
            print("Última exceção: " + str(type(lastException)) + " " + str(lastException))

        print("Trabalhando com " + str(len(self.interfaces)) + " interfaces")
        if len(self.interfaces) > 0:
            print(", ".join(self.interfaces))


    def getGateway(self):
        temp = ni.gateways()
        if 0 == len(temp['default']):
            return None
        idxNicGW = list(temp['default'].keys())[0]
        #for key in temp:
        #    if key != 'default' and key != idxNicGW:
        #        raise RuntimeError("WARNING: More than one NIC with default gateway")
        return ni.gateways()['default'][idxNicGW][0]

    def getNICGateway(self):
        return ni.gateways()['default'][list(ni.gateways()['default'].keys())[0]][1]

    #TODO Add a method to get the MAC address of the NICs

    #TODO Add a method to get the Subrange in the CIDR notation of each NIC, this will be useful for the ARP Spoofing
