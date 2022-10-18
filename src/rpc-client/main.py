import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://0.0.0.0:9000')

string = "hello world"

print(f" > {server.string_reverse(string)}")
print(f" > {server.string_length(string)}")