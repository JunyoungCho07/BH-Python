import socket

HOST = "127.0.0.1"
PORT = 9998

#made socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client connect
client.connect((HOST,PORT))

#send some data
client.send(b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')#\r\n -> like enter key
# client.send(b'Hello I am Junyoung, connecting to your server by tcp')

#recieve data
responce = client.recv(4096)

print(responce.decode('utf-8'))
client.close()

#nc -nlvp 9998