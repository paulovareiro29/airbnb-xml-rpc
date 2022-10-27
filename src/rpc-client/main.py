import xmlrpc.client
import os


def clear(): return os.system("clear")


clear()
print("Connecting to server...")
server = xmlrpc.client.ServerProxy('http://0.0.0.0:9000')
print("Connected!\n")


def importFile():
    print("Sending file..")
    filename = "airbnb-nyc-data.csv"

    with open(filename, "rb") as file:
        server.import_airbnb_data(xmlrpc.client.Binary(file.read()))
        file.close()
        print("File sent")


def handleExit():
    raise SystemExit


menu_options = {
    "1": ("Import file", importFile),
    "0": ("Exit", handleExit)
}


def menu():
    while True:
        print("RPC Client Menu:")
        for (key, option) in menu_options.items():
            print(f"   - [{key}] {option[0]}")

        opc = input("Choose an option: ")
        result = menu_options.get(opc)
        if result != None:
            result[1]()
        else:
            print("Invalid option! Try again!")

        input("Press any key to continue...")
        clear()


menu()
