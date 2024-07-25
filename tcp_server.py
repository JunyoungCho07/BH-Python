import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5) #how many connection this server support up to 
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        client, address = server.accept() #accept the connection -> return client , adress 
        print(f'[*] Accepted connection from {address[0]}:{address[1]}') #address[0] -> IP, adress[1] -> Port
        client_handler = threading.Thread(target=handle_client, args=(client,)) #??????
        client_handler.start() #?????


def handle_client(client_socket):
    with client_socket as sock: #what is this code doing?? I guess client_socket -> sock
        request = sock.recv(1024) #receive data
        print(f'[*] Received: {request.decode("utf-8")}') #print it
        sock.send(b'ACKKK') #send data to client
        # sock.send(b'I have successfuly received your data')


if __name__ == '__main__':
    main()
