import sys
import os
import yaml
import logging
import logging.config
import traceback

import time
import math
import copy
import json

# from telemetry_f1_2021.packets import PacketHeader, HEADER_FIELD_TO_PACKET_TYPE, PacketTestData
# from telemetry_f1_2022.packets import PacketHeader, HEADER_FIELD_TO_PACKET_TYPE, PacketTestData

import f1sim

import socket
import socketserver
import threading
import pika
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
import pickle
 
gamehost = None;
devicename = None;
config = None;
currentSession = {};
ts = 0;
lapNumber = 1;
lapSession = None;
trackName = None;
sector1_time = None;
sector2_time = None;
invalid_lap = None;

# PacketHeader = f1sim.loadclass("telemetry_f1_2021.packets.PacketHeader")
# PacketTestData = f1sim.loadclass("telemetry_f1_2021.packets.PacketTestData")
# HEADER_FIELD_TO_PACKET_TYPE = f1sim.loadclass("telemetry_f1_2021.packets.HEADER_FIELD_TO_PACKET_TYPE")
# HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE = f1sim.loadclass("telemetry_f1_2021.packets.HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE")
# TRACKS = f1sim.loadclass("telemetry_f1_2021.packets.TRACKS")

SAVE_DATA = True;      # Turn on for save data to cloud
FILTER_DATA = True;
VERSION = 2021;

# Create a tuple with IP Address and Port Number
ServerAddress = ("0.0.0.0", 20777)

try:
    device = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    device.connect(("8.8.8.8", 80))
    deviceip = device.getsockname()[0]
finally:
    device.close()

def find_packet_by_bestfit(key,data):
    bestfit = None
    packet = None
    for ii in HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE.keys():
        if key[0] == ii[0] and key[1] == ii[1] and key[2] == ii[2] and key[3] >= ii[3] and key[4] >= ii[4]:
            bestfit = ii
    if bestfit != None:
        packet = HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE[bestfit].from_buffer_copy(data)
    return packet

def read_socket():
    global STORE_TYPE
    global handler
    # Create a Server Instance
    if STORE_TYPE != "none":
        handler = f1sim.loadclass(config[STORE_TYPE]["fullclassname"])(config[STORE_TYPE]["properties"])
    if STORE_TYPE == "rabbitmq":
        # Non-Threading Version
        packetserver = socketserver.UDPServer(ServerAddress, PacketUDPRequestHandler)
    else:
        # Threading Version
        packetserver = socketserver.ThreadingUDPServer(ServerAddress, PacketUDPRequestHandler)
    # Make the server wait forever serving connection
    logging.info('Starting listener on 0.0.0.0:20777')
    packetserver.serve_forever()

class PacketUDPRequestHandler(socketserver.DatagramRequestHandler):

    # Override the handle() method
    def handle(self):
        global deviceip
        data = None
        header = None
        key = None
        try:
            data = self.rfile.read(2048).strip()
            header = PacketHeader.from_buffer_copy(data)
            key = (header.m_packet_format, header.m_packet_version, header.m_packet_id, header.m_game_major_version, header.m_game_minor_version)
            packet = find_packet_by_bestfit(key,data)
            if packet == None:
                key = (header.m_packet_format, header.m_packet_version, header.m_packet_id)
                packet = HEADER_FIELD_TO_PACKET_TYPE[key].from_buffer_copy(data)
            read_data_inf(deviceip,self.client_address[0],packet)
        except Exception as ex:
            logging.error(ex)
            if key == None:
                key = "Unknown"
            logging.error("Dropping packet: "+str(key))
            m_timestamp = math.trunc(time.time_ns() / 1000000)
            if header == None:
                session = "NaN"
                packet_id = "NaN"
            else:
                logging.error("Game Version: "+str((header.m_game_major_version, header.m_game_minor_version)))
                session = header.m_session_uid
                packet_id = header.m_packet_id
            if os.path.exists('errors/'+str(session)) == False:
                # Create a new directory because it does not exist
                os.makedirs('errors/'+str(session))
            if data == None:
                data = ""
            with open(f'errors/{session}/{session}-{packet_id}-{m_timestamp}.pickle', 'wb') as fh:
                pickle.dump(data, fh, protocol=pickle.HIGHEST_PROTOCOL)

def read_queue():
    global config
    global FORWARD_TYPE
    poolsize = 1
    if FORWARD_TYPE != 'none':
        if "poolsize" in config[FORWARD_TYPE]['properties']:
            poolsize = config[FORWARD_TYPE]['properties']['poolsize']
        handler = f1sim.loadclass(config[FORWARD_TYPE]["fullclassname"])(config[FORWARD_TYPE]["properties"])
        with ThreadPoolExecutor(max_workers=poolsize) as executor:
            fs = [executor.submit(consume_packet,handler) for i in range(poolsize)]
            wait(fs)

def consume_packet(handler):
    global config
    global FORWARD_TYPE
    properties = config[STORE_TYPE]['properties']
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=properties['host'], heartbeat=600, blocked_connection_timeout=300))
    channel = connection.channel()
    # declare our queues
    # channel.queue_declare(queue='PacketData')
    logging.info('Starting listener on '+STORE_TYPE+'@'+properties['host'])
    for method_frame, props, data in channel.consume('PacketData'):
        logging.debug("Received packet: "+props.headers['location']);
        # Display the message parts and acknowledge the message
        try:
            if FORWARD_TYPE == "local":
                header = PacketHeader.from_buffer_copy(data)
                key = (header.m_packet_format, header.m_packet_version, header.m_packet_id, header.m_game_major_version, header.m_game_minor_version)
                packet = find_packet_by_bestfit(key,data)
                if packet == None:
                    key = (header.m_packet_format, header.m_packet_version, header.m_packet_id)
                    packet = HEADER_FIELD_TO_PACKET_TYPE[key].from_buffer_copy(data)
            else:
                packet = data
            handler.insert(config[FORWARD_TYPE]['properties'][props.headers['location']+'data_info'], [packet])
        except Exception as ex:
            logging.error(ex)
        channel.basic_ack(method_frame.delivery_tag)
    connection.close()

# options are none, oracledb, local, rabbitmq, oss
STORE_TYPE=None
FORWARD_TYPE=None
CLIENT_TYPE=None
handler=None

# get data and insert it into database.
def main():
    global gamehost
    global devicename
    global config
    global handler
    global STORE_TYPE
    global FORWARD_TYPE
    global CLIENT_TYPE
    global SAVE_DATA
    global FILTER_DATA
    global VERSION
    global PacketHeader
    global PacketTestData
    global HEADER_FIELD_TO_PACKET_TYPE
    global HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE
    global TRACKS
    global trackName

    with open('f1log.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    with open('f1store.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
    VERSION = str(config['version'])
    PacketHeader = f1sim.loadclass("telemetry_f1_"+VERSION+".packets.PacketHeader")
    PacketTestData = f1sim.loadclass("telemetry_f1_"+VERSION+".packets.PacketTestData")
    HEADER_FIELD_TO_PACKET_TYPE = f1sim.loadclass("telemetry_f1_"+VERSION+".packets.HEADER_FIELD_TO_PACKET_TYPE")
    HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE = f1sim.loadclass("telemetry_f1_"+VERSION+".packets.HEADER_FIELD_TO_PACKET_TYPE_OVERRIDE")
    TRACKS = f1sim.loadclass("telemetry_f1_"+VERSION+".packets.TRACKS")
    gamehost = config['gamehost']
    devicename = config['devicename']
    SAVE_DATA = config['save']
    FILTER_DATA = config['filter']
    logging.info('Registered as ' + gamehost + '(' + devicename + ')');
    logging.info('Save Data: '+str(SAVE_DATA));
    logging.info('Filter Data: '+str(FILTER_DATA));
    STORE_TYPE = config['store']
    logging.info('Store configured: ' + STORE_TYPE);
    FORWARD_TYPE = config['forward']
    CLIENT_TYPE = sys.argv[1];
    if FORWARD_TYPE != "none":
        logging.info('Forward configured: ' + FORWARD_TYPE + '(' + CLIENT_TYPE + ')');
    else:
        logging.info('Forward (disabled)');
    try:
        if CLIENT_TYPE == "consume":
            read_queue()
        else:
            read_socket()
    except Exception as ex:
        logging.error(ex)
        logging.warning('Stop the car, stop the car Checo.')
        logging.warning('Stop the car, stop at pit exit.')
        logging.warning('Just pull over to the side.')

def read_data_inf(deviceip, clientip, packet):
    global handler
    try:
        logging.debug("Received packet: "+str(packet.m_header.m_packet_id));
        # logging.info("Packet Received");
        # ts stores the time in milliseconds (converted from nanoseconds)
        ts = math.trunc(time.time_ns() / 1000000)
        # test data packet
        if (packet.m_header.m_packet_format, packet.m_header.m_packet_version, packet.m_header.m_packet_id) == (0,0,0):
            save_testdata_packet(deviceip, clientip, ts, 'test', handler, packet)
        elif packet.m_header.m_packet_id == 0:
            # logging.info("Received packet: "+str(packet.m_header.m_packet_id));
            save_motiondata_packet(deviceip, clientip, ts, 'motion', handler, packet)
        elif packet.m_header.m_packet_id == 6:
            # logging.info("Received packet: "+str(packet.m_header.m_packet_id));
            save_telemetrydata_packet(deviceip, clientip, ts, 'telemetry', handler, packet)
        elif packet.m_header.m_packet_id == 2:
            # logging.info("Received packet: "+str(packet.m_header.m_packet_id));
            save_lapdata_packet(deviceip, clientip, ts, 'lap', handler, packet)
        elif packet.m_header.m_packet_id == 1:
            # logging.info("Received packet: "+str(packet.m_header.m_packet_id));
            save_sessiondata_packet(deviceip, clientip, ts, 'session', handler, packet)
        else:
            save_alldata_packet(deviceip, clientip, ts, str(packet.m_header.m_packet_id), handler, packet)
    except Exception as ex:
        logging.debug("Exception: "+str(ex));

def save_testdata_packet(deviceip, clientip, ts, stream, handler, packet):
    global config
    global gamehost
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    try:
        logging.debug("TEST: TEST DATA: ");
        if SAVE_DATA and STORE_TYPE != "none":
            if STORE_TYPE == "local" or FORWARD_TYPE == "local":
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], packet)
            else:
                test_data = packet.to_dict()
                test_data['m_timestamp'] = ts
                test_data['m_gamehost'] = gamehost
                test_data['m_devicename'] = devicename
                test_data['m_deviceip'] = deviceip
                data = json.dumps(test_data)
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], data)
        else:
            logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier) + "\", \"m_session\": \""+str(packet.m_header.m_session_uid) + "\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);
        traceback.print_exc()
        
def save_lapdata_packet(deviceip, clientip, ts, stream, handler, packet):
    global config
    global gamehost
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    try:
        logging.debug("1: Incoming Lap: " + str(packet.m_lap_data[0]));
        lap_data = None
        if SAVE_DATA and STORE_TYPE != "none":
            if STORE_TYPE == "local" or FORWARD_TYPE == "local":
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], packet)
            else:
                if FILTER_DATA:
                    lap_data = {
                        "m_timestamp": ts,
                        "m_gamehost": gamehost,
                        "m_frame": packet.m_header.m_frame_identifier,
                        "m_session": packet.m_header.m_session_uid, 
                        "m_driver_status": packet.m_lap_data[0].m_driver_status,
                        "m_totalDistance" : packet.m_lap_data[0].m_total_distance,
                        "m_sector1_time_in_ms" : packet.m_lap_data[0].m_sector1_time_in_ms,
                        "m_sector2_time_in_ms" : packet.m_lap_data[0].m_sector2_time_in_ms,
                        "m_last_lap_time_in_ms": packet.m_lap_data[0].m_last_lap_time_in_ms,
                        "m_lap_distance": packet.m_lap_data[0].m_lap_distance,
                        "m_sector": packet.m_lap_data[0].m_sector,
                        "m_current_lap_time_in_ms" : packet.m_lap_data[0].m_current_lap_time_in_ms,
                        "m_current_lap_num": packet.m_lap_data[0].m_current_lap_num,
                        "m_current_lap_invalid": packet.m_lap_data[0].m_current_lap_invalid,
                    };
                    # Process Lap Time Data
                    process_laptime(lap_data)

                else:
                    lap_data = packet.to_dict()
                    lap_data['m_timestamp'] = ts
                    lap_data['m_gamehost'] = gamehost

                data = json.dumps(lap_data)
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], data)
        else:
            logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier) + "\", \"m_session\": \""+str(packet.m_header.m_session_uid) + "\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);
        traceback.print_exc()
        
def save_telemetrydata_packet(deviceip, clientip, ts, stream, handler, packet):
    global config
    global gamehost
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    try:
        logging.debug("3. Incoming Telemetry: " + str(packet.m_car_telemetry_data[0]));
        if SAVE_DATA and STORE_TYPE != "none":
            if STORE_TYPE == "local" or FORWARD_TYPE == "local":
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], packet)
            else:
                if FILTER_DATA:
                    telemetry_data = {
                        "m_timestamp": ts,
                        "m_gamehost": gamehost,
                        "m_frame": packet.m_header.m_frame_identifier,
                        "m_session": packet.m_header.m_session_uid,
                        "m_speed": packet.m_car_telemetry_data[0].m_speed,
                        "m_throttle": packet.m_car_telemetry_data[0].m_throttle,
                        "m_brake": packet.m_car_telemetry_data[0].m_brake,
                        "m_gear": packet.m_car_telemetry_data[0].m_gear,
                        "m_drs": packet.m_car_telemetry_data[0].m_drs,
                        "m_steer": packet.m_car_telemetry_data[0].m_steer,
                        "m_engineRPM": packet.m_car_telemetry_data[0].m_engine_rpm,
                        "m_engine_temperature": packet.m_car_telemetry_data[0].m_engine_temperature,
                        "m_brakes_temperature": [ packet.m_car_telemetry_data[0].m_brakes_temperature[i] for i in range(4) ],
                        "m_tyres_surface_temperature": [ packet.m_car_telemetry_data[0].m_tyres_surface_temperature[i] for i in range(4) ],
                        "m_tyres_inner_temperature": [ packet.m_car_telemetry_data[0].m_tyres_inner_temperature[i] for i in range(4) ],
                        "m_tyres_pressure": [ packet.m_car_telemetry_data[0].m_tyres_pressure[i] for i in range(4) ],
                    };
                else:
                    telemetry_data = packet.to_dict()
                    telemetry_data['m_timestamp'] = ts
                    telemetry_data['m_gamehost'] = gamehost

                data = json.dumps(telemetry_data)
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], data)
        else:
            logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier) + "\", \"m_session\": \""+str(packet.m_header.m_session_uid) + "\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);
        traceback.print_exc()
        
def save_motiondata_packet(deviceip, clientip, ts, stream, handler, packet):
    global config
    global gamehost
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    try:
        logging.debug("2. Incoming Motion: " + str(packet.m_car_motion_data[0]));
        if SAVE_DATA and STORE_TYPE != "none":
            if STORE_TYPE == "local" or FORWARD_TYPE == "local":
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], packet)
            else:
                if FILTER_DATA:
                    motion_data = {
                        "m_timestamp": ts,
                        "m_gamehost": gamehost,
                        "m_frame": packet.m_header.m_frame_identifier,
                        "m_session": packet.m_header.m_session_uid,
                        "m_worldPosX": packet.m_car_motion_data[0].m_world_position_x * -1,
                        "m_worldPosY": packet.m_car_motion_data[0].m_world_position_z,
                        "m_worldPosZ": packet.m_car_motion_data[0].m_world_position_y,
                        "worldForwardDirX": packet.m_car_motion_data[0].m_world_forward_dir_x,
                        "worldForwardDirY": packet.m_car_motion_data[0].m_world_forward_dir_y,
                        "worldForwardDirZ": packet.m_car_motion_data[0].m_world_forward_dir_z,
                        "worldRightDirX": packet.m_car_motion_data[0].m_world_right_dir_x,
                        "worldRightDirY": packet.m_car_motion_data[0].m_world_right_dir_y,
                        "worldRightDirZ": packet.m_car_motion_data[0].m_world_right_dir_z,
                        "m_yaw": packet.m_car_motion_data[0].m_yaw,
                        "m_pitch": packet.m_car_motion_data[0].m_pitch,
                        "m_roll": packet.m_car_motion_data[0].m_roll,
                        "m_front_wheels_angle": packet.m_front_wheels_angle,
                    };
                else:
                    motion_data = packet.to_dict()
                    motion_data['m_timestamp'] = ts
                    motion_data['m_gamehost'] = gamehost

                data = json.dumps(motion_data)
                save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], data)
        else:
            logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier) + "\", \"m_session\": \""+str(packet.m_header.m_session_uid) + "\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);
        traceback.print_exc()

def save_sessiondata_packet(deviceip, clientip, ts, stream, handler, packet):
    global currentSession
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    global trackName

    global lapNumber
    global lapSession  

    try:
        if (clientip in currentSession) == False or currentSession[clientip] != packet.m_header.m_session_uid:
            currentSession[clientip] = packet.m_header.m_session_uid;
            logging.info("New Session {} for IP {}".format(currentSession[clientip],clientip));

            # Reset Laptime Globals
            lapNumber =1;
            lapSession = None;

            if SAVE_DATA and STORE_TYPE != "none":
                if STORE_TYPE == "local" or FORWARD_TYPE == "local":
                    save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], packet)
                else:
                    if FILTER_DATA:
                        session_data = {
                            "m_timestamp": ts,
                            "m_gamehost": gamehost,
                            "m_devicename": devicename,
                            "m_session": packet.m_header.m_session_uid,
                            "m_packet_format": packet.m_header.m_packet_format,
                            "m_game_major_version": packet.m_header.m_game_major_version,
                            "m_game_minor_version": packet.m_header.m_game_minor_version,
                            "m_trackid": TRACKS[packet.m_track_id]["name"],
                            "m_track_length": packet.m_track_length,
                        };
                    else:
                        session_data = packet.to_dict()
                        session_data['m_timestamp'] = ts
                        session_data['m_gamehost'] = gamehost
                        session_data['m_devicename'] = devicename

                    if trackName != TRACKS[packet.m_track_id]["name"]:
                        trackName = TRACKS[packet.m_track_id]["name"]

                    data = json.dumps(session_data)
                    logging.debug("\nJDB Session Data: " + data)
                    save_packet(stream, handler, config[STORE_TYPE]['properties'][stream+'data_info'], data)
            else:
                logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier) + "\", \"m_session\": \""+str(packet.m_header.m_session_uid) + "\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);

def save_alldata_packet(deviceip, clientip, ts, stream, handler, packet):
    global SAVE_DATA
    global FILTER_DATA
    global STORE_TYPE
    global trackName

    global lapNumber
    global lapSession  

    try:
        if SAVE_DATA and STORE_TYPE != "none":
            if STORE_TYPE == "local":
                save_packet(stream, handler, stream, packet)
        else:
            logging.info("captured: { \"m_frame\": \""+str(packet.m_header.m_frame_identifier)+"\", \"m_packet_id\": \""+str(packet.m_header.m_packet_id) + "\" }")
    except Exception as ex:
        logging.error(ex);

def save_packet(stream, handler, procedure, data):
    logging.debug("Outgoing Data Stream: " + stream + " == " + str(data));
    handler.insert(procedure, [data])

def process_laptime(lapdata):

    global lapNumber
    global lapSession
    global sector1_time
    global sector2_time
    global invalid_lap
    global trackName

    # New Lap, for same session then create Lap Time Record
    if lapdata["m_current_lap_num"] > lapNumber and lapdata["m_session"] == lapSession:
        laptimePacket = {}
        laptimePacket["m_session"] = lapdata["m_session"]
        laptimePacket["m_gamehost"] = lapdata["m_gamehost"]
        laptimePacket["m_trackid"] = trackName
        laptimePacket["m_packet_format"] = VERSION
        laptimePacket["lap_num"] = lapNumber
        laptimePacket["lap_time_in_ms"] = lapdata["m_last_lap_time_in_ms"]
        laptimePacket["sector1_in_ms"] = sector1_time
        laptimePacket["sector2_in_ms"] = sector2_time
        laptimePacket["sector3_in_ms"] = (lapdata["m_last_lap_time_in_ms"] - sector1_time - sector2_time)
        laptimePacket["invalid_lap"] = invalid_lap

        logging.debug("Laptime: " + str(laptimePacket))

        # Filter out incomplete laps
        if lapdata["m_last_lap_time_in_ms"] > 0 and sector1_time > 0 and sector2_time > 0:
            data = json.dumps(laptimePacket)
            save_packet("laptime", handler, config[STORE_TYPE]['properties']['laptimedata_info'], data)

        lapNumber = lapdata["m_current_lap_num"]

    # Reset Values to new lap(stored as last lap detail)
    sector1_time = lapdata["m_sector1_time_in_ms"]
    sector2_time = lapdata["m_sector2_time_in_ms"]
    invalid_lap = lapdata["m_current_lap_invalid"]
    lapSession = lapdata["m_session"]

if __name__ == '__main__':
    main()
