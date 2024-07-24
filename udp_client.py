#User Datagram Protocol
import socket

HOST = '127.0.0.1'
PORT = 9997

#create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Datagram -> UDP

#Send some data
client.sendto(b'AAABBBCCC', (HOST, PORT))

#Receive some data
data, address = client.recvfrom(4096)
print(data.decode('utf-8'))
print(address.decode('utf-8'))
client.close()

#nc -ulp 9997