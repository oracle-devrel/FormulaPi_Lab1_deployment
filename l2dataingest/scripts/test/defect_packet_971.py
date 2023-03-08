import sys
import os
import glob
import time
import socket
import pickle
import json
import queue
import logging

from telemetry_f1_2022.packets import PacketHeader, HEADER_FIELD_TO_PACKET_TYPE, HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE, PacketLapData_v2022_1_8, PacketLapData

q = queue.Queue()
socketclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
localudpclient = (sys.argv[1], 20777)
timestamp = None
start = None

def send():
    global start
    global timestamp
    global socketclient
    global localudpclient 
    data = bytes(972)
    packet = PacketLapData.from_buffer_copy(data)
    header = packet.m_header;
    header.m_packet_format = 2022
    header.m_packet_version = 1
    header.m_packet_id = 2
    header.m_game_major_version = 1
    header.m_game_minor_version = 7
    print(packet)
    # Send to server using created UDP socket
    socketclient.sendto(packet.pack(), localudpclient)

def main():
    global start
    send()

if __name__ == '__main__':
    main()
