import detectHosts
import OwnInformation

# OwnInformation pega as informações de rede do prórpio host
#TODO fazer pegar o endereço MAC
ownInformation = OwnInformation.managerDevice()
ownInformation.print_table()


# detectHosts pega as informações de hosts na rede
detectHosts = detectHosts.detectHosts()
detectHosts.bySubrange("10.1.1.0/24")

