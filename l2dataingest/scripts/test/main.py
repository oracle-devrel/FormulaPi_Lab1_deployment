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

def send(tuple):
    global start
    global timestamp
    global socketclient
    global localudpclient 
    current_timestamp = tuple[0]
    if timestamp == None:
        timestamp = current_timestamp;
    delta_timestamp = (current_timestamp - timestamp) / 1000000
    packet = tuple[1]
    current_time = time.time_ns()
    delta_time = (current_time - start) / 1000000
    if (delta_timestamp > delta_time):
        time.sleep((delta_timestamp - delta_time)/1000)
    # Send to server using created UDP socket
    packet.m_header.m_session_uid = start
    print(str(packet.m_header.m_session_uid)+":"+str(packet.m_header.m_packet_id)+":"+str(packet.m_header.m_frame_identifier))
    socketclient.sendto(packet.pack(), localudpclient)

def read_and_queue(filename):
    global q
    with open(filename, "rb") as input_file:
        data = pickle.load(input_file) 
        current_timestamp = int(filename[filename.rfind('-')+1:filename.find('.pickle')])
        q.put((current_timestamp,data))

def sort_by_filename_timestamp(filename):
    # 9038508826540061828-telemetry-1655937106567290379.pickle
    return filename[filename.rfind('-')+1:filename.find('.pickle')]

def print_help():
    print("Help: (Sample)")
    print("Syntax: test/main.py hostname testdir")
    print("hostname: IP address of the UDP listener (with default port of 20777)")
    print("testdir: directory where the series of pickle files will be read from.")
    print("NB: Assume that the filename format (and origin) of pickle files are from the f1sim-consumer.")
    print("")
    print(". dev/bin/activate")
    print(". f1env.sh")
    print("python3 test/main.py localhost test/data/123")

def main():
    global start
    try:
        data_dir = sys.argv[2]
        glob_results = glob.glob(data_dir+'/*.pickle')
        glob_results = sorted(glob_results,key=sort_by_filename_timestamp)
        for g in glob_results:
            read_and_queue(g)
        start = time.time_ns()
        while q.empty() == False:
            send(q.get())
            q.task_done()
    except:
        print_help()

if __name__ == '__main__':
    main()
