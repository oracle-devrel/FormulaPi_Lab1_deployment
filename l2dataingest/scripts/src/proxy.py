import socket
import socketserver
import threading
import sys

# Create a tuple with IP Address and Port Number
ServerAddress = (sys.argv[1], 20777)

# Create a tuple with IP Address and Port Number
ClientAddress = (sys.argv[2], 20777)

socketclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def read_socket():
    packetserver = socketserver.ThreadingUDPServer(ServerAddress, PacketUDPRequestHandler)
    # Make the server wait forever serving connection
    print('Starting listener on '+sys.argv[1]+':20777')
    print('Forwarding to '+sys.argv[2]+':20777')
    packetserver.serve_forever()

class PacketUDPRequestHandler(socketserver.DatagramRequestHandler):

    # Override the handle() method
    def handle(self):
        data = self.rfile.read(2048).strip()
        # print(data)
        socketclient.sendto(data, ClientAddress)

def main():
    try:
        read_socket()
    except Exception as ex:
        print(ex)
        print('Stop the car, stop the car Checo.')
        print('Stop the car, stop at pit exit.')
        print('Just pull over to the side.')

if __name__ == '__main__':
    main()
