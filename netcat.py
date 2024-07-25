import argparse #command line argument
import socket
import shlex
import subprocess
import sys #system commands
import textwrap 
import threading #multi threading


def execute(cmd): #cmd -> string
    cmd = cmd.strip() #sript it in case commend include extra spaces
    if not cmd: #no commend
        return
    output = subprocess.check_output(shlex.split(cmd),
                                     stderr=subprocess.STDOUT) #incoded output
    return output.decode() #decoded output


class NetCat:
    def __init__(self, args, buffer=None): #self -> this
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()# -l option
        else:
            self.send()# if not listener, use send function

    def send(self):
        self.socket.connect((self.args.target, self.args.port)) #connection to the target
        if self.buffer: #if there is anything in the buffer
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len: #untill no data to read(read all the data in and appending th the responce)
                    data = self.socket.recv(4096) #recived data > data
                    recv_len = len(data) #length of the data > recv_len
                    response += data.decode() #append the decoded data > responce
                    if recv_len < 4096: #????????????? why break it ?????????
                        break
                if response:
                    print(response)
                    buffer = input('> ') #print it out to the console
                    buffer += '\n' #new line
                    self.socket.send(buffer.encode()) #encode the buffer and send it
        except KeyboardInterrupt: #ctrl + c -> stoping netcat
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        print('listening')
        self.socket.bind((self.args.target, self.args.port)) #bind???????????
        self.socket.listen(5) #support up to 5 connection at once
        while True:
            client_socket, _ = self.socket.accept() #listening continuously
            client_thread = threading.Thread(target=self.handle, args=(client_socket,)) #pick up the connection
            client_thread.start() #start the thread

    def handle(self, client_socket):
        #correspond to each flag(arguments)
        if self.args.execute: #if execute flag
            output = execute(self.args.execute) #execute the command(self.args.execute -> command)
            client_socket.send(output.encode())
        
        elif self.args.upload: #-u
            file_buffer = b'' #inicialize file buffer
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data #add recieved data
                    print(len(file_buffer)) #print length of the data
                else:
                    break

            with open(self.args.upload, 'wb') as f: #write to the file
                f.write(file_buffer) #save the file
            message = f'Saved file {self.args.upload}' #file name
            client_socket.send(message.encode()) #?????????????????????

        elif self.args.command:
            cmd_buffer = b''#???????????
            while True:
                try:
                    client_socket.send(b' #> ')
                    while '\n' not in cmd_buffer.decode(): #\n -> new line -> command finished
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response: # if there is the responce
                        client_socket.send(response.encode()) #encode and send it off to the client
                    cmd_buffer = b''#???????????
                except Exception as e: #?????????????????
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
          netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
          netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.whatisup # upload to file
          netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
          echo 'ABCDEFGHI' | ./netcat.py -t 192.168.1.108 -p 135 # echo local text to server port 135
          netcat.py -t 192.168.1.108 -p 5555 # connect to server
          '''))

    #create arguments
    parser.add_argument('-c', '--command', action='store_true', help='initialize command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen: #-l, --listen option
        buffer = '' #empty buffer
    else:
        buffer = sys.stdin.read() # standard in -> stdin

    #passing data in 
    nc = NetCat(args, buffer.encode('utf-8')) # pass command line arguments, encode it to upass the data nicely
    nc.run()
