import signal
from xmlrpc.client import Fault, Binary, ServerProxy
import os
import sys


def clear(): return os.system("clear")


clear()
print("Connecting to server...")
server = ServerProxy('http://0.0.0.0:9000')
print("Connected!\n")


def listDocuments():
    documents = server.index()
    if len(documents) > 0:
        print("Listing all documents:")
        for doc in documents:
            print(f"  - {doc[1]}")
        return len(documents)
    else:
        print("Documents list is empty!")
        return 0


def importDocument():
    filename = input("Insert filename: ")

    if not filename.strip():
        print("No document was selected...")
        return

    try:
        with open(filename, "rb") as file:
            print("Importing file..")

            try:
                server.insert(
                    filename, Binary(file.read()))
                print("File imported!")
            except Fault as error:
                print(error.faultString)
            finally:
                file.close()
    except FileNotFoundError as _:
        print("File not found!")


def deleteDocument():
    size = listDocuments()

    if size > 0:
        filename = input("\nInsert filename: ")

        if not filename.strip():
            print("No document was selected...")
            return

        try:
            server.delete(filename)
            print(f"Document '{filename}' has been deleted successfuly!")
        except Fault as e:
            print(e.faultString)


def handleExit(signum=None, frame=None):
    sys.exit(0)


signal.signal(signal.SIGTERM, handleExit)
signal.signal(signal.SIGHUP, handleExit)
signal.signal(signal.SIGINT, handleExit)


menu_options = {
    "1": ("List all Documents", listDocuments),
    "2": ("Import Document", importDocument),
    "3": ("Delete Document", deleteDocument),
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
            clear()
            result[1]()
        else:
            print("Invalid option! Try again!")

        input("\nPress any key to continue...")
        clear()


menu()
