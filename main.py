import detectHosts
import OwnInformation
import aux

# OwnInformation pega as informações de rede do prórpio host
#TODO fazer pegar o endereço MAC
ownInformation = OwnInformation.managerDevice()
ownInformation.print_table()
IPs = ownInformation.getIP()
masks = ownInformation.getNetworkRange()

informations = {}
for i in range(len(IPs)):
    detectHosts = detectHosts.detectHosts(IPs[i], masks[i])
    detectHosts.printTable()
    informations = detectHosts.getInformations()

jsonFile = "./output.json"
data = aux.loadData(jsonFile)
aux.addContent(data, informations)
aux.saveData(jsonFile, data)