import sys
import os
import socket

from telemetry_f1_2021.packets import PacketTestData

socketclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
localudpclient = ("127.0.0.1", 20777)

def main():
    data = bytes(48)
    testdata = PacketTestData.from_buffer_copy(data)
    socketclient.sendto(testdata.pack(), localudpclient)

if __name__ == '__main__':
    main()
