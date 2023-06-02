import sys
import os
import glob
import time
import socket
import pickle
import json
import queue
import logging

q = queue.Queue()
timestamp = None
start = None
from telemetry_f1_2022.packets import PacketHeader, PacketEventData_v2022_1_9, HEADER_FIELD_TO_PACKET_TYPE, HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE

def find_packet_by_bestfit(key,data):
    bestfit = None
    packet = None
    for ii in HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE.keys():
        if key[0] == ii[0] and key[1] == ii[1] and key[2] == ii[2] and key[3] >= ii[3] and key[4] >= ii[4]:
            bestfit = ii
    if bestfit != None:
        packet = HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE[bestfit].from_buffer_copy(data)
    return packet

def read_and_queue(filename):
    global q
    with open(filename, "rb") as input_file:
        if filename.endswith(".pickle"):
            data = pickle.load(input_file) 
            print("PICKLE {}".format(data))
            packet = PacketHeader.from_buffer_copy(data)
            print("PACKET {}".format(packet))
            key = (packet.m_packet_format, packet.m_packet_version, packet.m_packet_id, packet.m_game_major_version, packet.m_game_minor_version)
            packet = find_packet_by_bestfit(key,data)
            print("PACKET {}".format(packet))
        elif filename.endswith(".bytes"):
            data = input_file.read()
            print(data)
            packet = PacketHeader.from_buffer_copy(data)
            print(packet)
            key = (packet.m_packet_format, packet.m_packet_version, packet.m_packet_id, packet.m_game_major_version, packet.m_game_minor_version)
            packet = find_packet_by_bestfit(key,data)
            print("PACKET {}".format(packet))

def main():
    global start
    # try:
    read_and_queue(sys.argv[1])
    # except:
    #     pass

if __name__ == '__main__':
    main()
