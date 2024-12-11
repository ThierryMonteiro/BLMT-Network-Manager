import detectHosts
import OwnInformation
import auxi
import asyncio

# OwnInformation pega as informações de rede do prórpio host

async def main():

    ownInformation = OwnInformation.managerDevice()
    ownInformation.print_table()
    IPs = ownInformation.ips
    masks = ownInformation.getNetworkRange()

    informations_list = []

    for i in range(len(IPs)):
        if i == 0:
            detectedHosts = detectHosts.detectHosts(IPs[i], masks[i])
            detectedHosts.printTable()
            informations_list.append(await detectedHosts.getInformations())

    print("Informações dos hosts detectados:")

    jsonFile = "./output.json"
    data = auxi.loadData(jsonFile)
    for info in informations_list:
        auxi.addContent(data, info)
    auxi.saveData(jsonFile, data)

    auxi.printLogTable("./output.json")
    auxi.printDevicesTable("./currentChanges.json")


if __name__ == "__main__":
    asyncio.run(main())