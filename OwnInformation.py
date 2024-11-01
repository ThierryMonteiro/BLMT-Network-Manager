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
        # https://learn.microsoft.com/pt-br/windows-hardware/drivers/network/convertinterfacenametoluidw
        # https://learn.microsoft.com/pt-br/windows-hardware/drivers/network/convertinterfaceluidtonamew
        # https://github.com/python/cpython/blob/260843df1bd8a28596b9a377d8266e2547f7eedc/Modules/socketmodule.c#L7017C20-L7017C47
        # https://learn.microsoft.com/en-us/windows/win32/api/iptypes/ns-iptypes-ip_adapter_addresses_lh
        # https://learn.microsoft.com/en-us/windows/win32/api/iphlpapi/nf-iphlpapi-getadaptersaddresses
        # https://lib.rs/crates/get_adapters_addresses
        # https://github.com/SamuelYvon/netifaces-2/blob/edac9552b5c78ce21d4e0e652ca4502beeed7aa0/src/win.rs#L72
        # https://github.com/SamuelYvon/netifaces-2/blob/edac9552b5c78ce21d4e0e652ca4502beeed7aa0/src/win.rs#L115
        # Em resumo: no Windows, precisamos conviver com UUIDs no lugar dos nomes das interfaces.
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
        idxNicGW = list(temp['default'].keys())[0]
        #for key in temp:
        #    if key != 'default' and key != idxNicGW:
        #        raise RuntimeError("WARNING: More than one NIC with default gateway")
        return ni.gateways()['default'][idxNicGW][0]

    def getNICGateway(self):
        return ni.gateways()['default'][list(ni.gateways()['default'].keys())[0]][1]

    #TODO Add a method to get the MAC address of the NICs

    #TODO Add a method to get the Subrange in the CIDR notation of each NIC, this will be useful for the ARP Spoofing
