import sys
import os
import glob
import time
import socket
import pickle
import json
import queue
import logging

from telemetry_f1_2022.packets import PacketHeader, HEADER_FIELD_TO_PACKET_TYPE, HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE, PacketLapData_v2022_1_8, PacketMotionData

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
    #data = bytes(1347)
    filename = '/home/pi/f1-simulator/test/data/1656711700911627733/1656711700911627733-motion-1656711701939.pickle'
    with open(filename, "rb") as input_file:
        data = pickle.load(input_file)
        header = PacketHeader.from_buffer_copy(data)
        key = (header.m_packet_format, header.m_packet_version, header.m_packet_id, header.m_game_major_version, header.m_game_minor_version)
        print(key)
        if key in HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE:
            packet = HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE[key].from_buffer_copy(data)
        else:
            key = (header.m_packet_format, header.m_packet_version, header.m_packet_id)
            packet = HEADER_FIELD_TO_PACKET_TYPE[key].from_buffer_copy(data)
        print(packet)
    # Send to server using created UDP socket
    # socketclient.sendto(packet.pack(), localudpclient)
   
def main():
    global start
    send()

if __name__ == '__main__':
    main()
