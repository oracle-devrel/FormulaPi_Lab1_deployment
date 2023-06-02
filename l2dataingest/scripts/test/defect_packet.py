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
socketclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
localudpclient = (sys.argv[1], 20777)
timestamp = None
start = None

def send():
    global start
    global timestamp
    global socketclient
    global localudpclient 
    with open(sys.argv[2], "rb") as input_file:
        data = pickle.load(input_file)
        data.m_header.m_packet_id = 11
        # Send to server using created UDP socket
        socketclient.sendto(data.pack(), localudpclient)

def main():
    global start
    try:
        send()
    except:
        pass

if __name__ == '__main__':
    main()
