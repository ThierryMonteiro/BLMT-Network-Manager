import detectHosts
import OwnInformation
import aux
import asyncio

# OwnInformation pega as informações de rede do prórpio host

async def main():

    ownInformation = OwnInformation.managerDevice()
    ownInformation.print_table()
    IPs = ownInformation.getIP()
    masks = ownInformation.getNetworkRange()

    informations_list = []


    for i in range(len(IPs)):
        if i == 0:
            detectedHosts = detectHosts.detectHosts(IPs[i], masks[i])
            detectedHosts.printTable()
            informations_list.append(await detectedHosts.getInformations())

    print("Informações dos hosts detectados:")

    jsonFile = "./output.json"
    data = aux.loadData(jsonFile)
    for info in informations_list:
        aux.addContent(data, info)
    aux.saveData(jsonFile, data)



if __name__ == "__main__":
    asyncio.run(main())