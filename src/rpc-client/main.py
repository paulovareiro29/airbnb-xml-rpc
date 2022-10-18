import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://0.0.0.0:9000')


print("Sending file..")
filename = "airbnb-nyc-data.csv"

with open(filename, "rb") as file:
    server.import_airbnb_data(xmlrpc.client.Binary(file.read()))
    file.close()

print("File sent")
