import socket
HOST = "www.google.com"
PORT = 80
#made socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client connect
client.connect((HOST,PORT))
#send some data
client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')
#recieve data
responce = client.recv(4096)
print(responce.decode('utf-8'))
client.close()