import socket
import netifaces as ni
from prettytable import PrettyTable

class managerDevice:
    def __init__(self):
        self.interfaces = self.getInterfaces()
        self.ips = self.getIP()
        self.IPdict = self.getIPdict()
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

    # List the NICs of the manager device
    def getInterfaces(self):
        interfaces = []
        for interface in socket.if_nameindex():
            if interface[1] != 'lo':  # Removing loopback interface by hand
                interfaces.append(interface[1])
        return interfaces

    def getIP(self):
        ip = []
        for interface in self.interfaces:
            ip.append(ni.ifaddresses(interface)[ni.AF_INET][0]['addr'])
        return ip

    def getIPdict(self):
        ip_dict = {}
        for interface in self.interfaces:
            ip_dict[interface] = ni.ifaddresses(interface)[ni.AF_INET]
        return ip_dict

    def getGateway(self):
        temp = ni.gateways()
        idxNicGW = list(temp['default'].keys())[0]
        for key in temp:
            if key != 'default' and key != idxNicGW:
                raise RuntimeError("WARNING: More than one NIC with default gateway")
        return ni.gateways()['default'][idxNicGW][0]

    def getNICGateway(self):
        return ni.gateways()['default'][list(ni.gateways()['default'].keys())[0]][1]

    #TODO Add a method to get the MAC address of the NICs

    #TODO Add a method to get the Subrange in the CIDR notation of each NIC, this will be useful for the ARP Spoofing
