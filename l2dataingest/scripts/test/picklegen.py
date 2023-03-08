import sys
import os
import socket
import cx_Oracle
import logging
import json
import pickle

import f1sim

from telemetry_f1_2022.packets import HEADER_FIELD_TO_PACKET_TYPE, TRACKS, Packet, PacketTestData, PacketLapData

# HEADER_FIELD_TO_PACKET_TYPE = {
#     (0, 0, 0): PacketTestData,
#     (2021, 1, 0): PacketMotionData,
#     (2021, 1, 1): PacketSessionData,
#     (2021, 1, 2): PacketLapData,
#     (2021, 1, 3): PacketEventData,
#     (2021, 1, 4): PacketParticipantsData,
#     (2021, 1, 5): PacketCarSetupData,
#     (2021, 1, 6): PacketCarTelemetryData,
#     (2021, 1, 7): PacketCarStatusData,
#     (2021, 1, 8): PacketFinalClassificationData,
#     (2021, 1, 9): PacketLobbyInfoData,
#     (2021, 1, 10): PacketCarDamageData,
#     (2021, 1, 11): PacketSessionHistoryData,
# }
filedir = 'test/data'

def write_pickle(m_timestamp, packet_id, packetdata):
    try:
        session = packetdata.m_header.m_session_uid;
        if os.path.exists(filedir+'/'+str(session)) == False:
            # Create a new directory because it does not exist
            os.makedirs(filedir+'/'+str(session))
        with open(f'{filedir}/{session}/{session}-{packet_id}-{m_timestamp}.pickle', 'wb') as fh:
            pickle.dump(packetdata, fh, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        logging.error(ex)
        return -1
    return 1

def create_sessiondata_packet(packet):
    version = None
    if "m_packet_format" in packet:
        version = packet["m_packet_format"]
    else:
        version = 2021
    packetclass = f1sim.loadclass("telemetry_f1_"+str(version)+".packets.PacketSessionData")
    trackclass = f1sim.loadclass("telemetry_f1_"+str(version)+".packets.TRACKS")
    emptydata = bytes(packetclass.size())
    packetdata = packetclass.from_buffer_copy(emptydata)
    m_timestamp = None
    m_gamehost = None
    for i in packet:
        # print(i,packet[i])
        if i == "m_timestamp":
            m_timestamp = packet[i]
        elif i == "m_gamehost":
            m_gamehost = packet[i]
        elif i == "m_session":
            packetdata.m_header.m_session_uid = packet[i]
        elif i == "m_packet_format":
            packetdata.m_header.m_packet_format = packet[i]
        elif i == "m_game_major_version":
            packetdata.m_header.m_game_major_version = packet[i]
        elif i == "m_game_minor_version":
            packetdata.m_header.m_game_minor_version = packet[i]
        elif i == "m_trackid":
            for ii in range(len(trackclass)):
                if trackclass[ii]["name"] == packet[i]:
                    packetdata.m_track_id = ii
        elif i == "m_track_length":
            packetdata.m_track_length = packet[i]
    packetdata.m_header.m_packet_format = version
    packetdata.m_header.m_packet_version = 1
    packetdata.m_header.m_packet_id = 1
    write_pickle(m_timestamp,'session',packetdata)
    # print(packetdata)
    return version

def create_lapdata_packet(packet,version):
    packetclass = f1sim.loadclass("telemetry_f1_"+str(version)+".packets.PacketLapData")
    emptydata = bytes(packetclass.size())
    packetdata = packetclass.from_buffer_copy(emptydata)
    m_timestamp = None
    m_gamehost = None
    for i in packet:
        # print(i,packet[i])
        if i == "m_timestamp":
            m_timestamp = packet[i]
        elif i == "m_gamehost":
            m_gamehost = packet[i]
        elif i == "m_session":
            packetdata.m_header.m_session_uid = packet[i]
        elif i == "m_frame":
            packetdata.m_header.m_frame_identifier = packet[i]
        elif i == "m_current_lap_time_in_ms":
            packetdata.m_lap_data[0].m_current_lap_time_in_ms = packet[i]
        elif i == "m_totalDistance":
            packetdata.m_lap_data[0].m_total_distance = packet[i]
        elif i == "m_sector1_time_in_ms":
            packetdata.m_lap_data[0].m_sector1_time_in_ms = packet[i]
        elif i == "m_sector2_time_in_ms":
            packetdata.m_lap_data[0].m_sector2_time_in_ms = packet[i]
        elif i == "m_lap_distance":
            packetdata.m_lap_data[0].m_lap_distance = packet[i]
        elif i == "m_current_lap_num":
            packetdata.m_lap_data[0].m_current_lap_num = packet[i]
        elif i == "m_current_lap_invalid":
            packetdata.m_lap_data[0].m_current_lap_invalid = packet[i]
        elif i == "m_sector":
            packetdata.m_lap_data[0].m_sector = packet[i]
        elif i == "m_driver_status":
            packetdata.m_lap_data[0].m_driver_status = packet[i]
        elif i == "m_last_lap_time_in_ms":
            packetdata.m_lap_data[0].m_last_lap_time_in_ms = packet[i]
    packetdata.m_header.m_packet_format = version
    packetdata.m_header.m_packet_version = 1
    packetdata.m_header.m_packet_id = 2
    write_pickle(m_timestamp,'lap',packetdata)
    # print(packetdata)

def create_motiondata_packet(packet,version):
    packetclass = f1sim.loadclass("telemetry_f1_"+str(version)+".packets.PacketMotionData")
    emptydata = bytes(packetclass.size())
    packetdata = packetclass.from_buffer_copy(emptydata)
    m_timestamp = None
    m_gamehost = None
    for i in packet:
        # print(i,packet[i])
        if i == "m_timestamp":
            m_timestamp = packet[i]
        elif i == "m_gamehost":
            m_gamehost = packet[i]
        elif i == "m_session":
            packetdata.m_header.m_session_uid = packet[i]
        elif i == "m_frame":
            packetdata.m_header.m_frame_identifier = packet[i]
        elif i == "m_worldPosX":
            packetdata.m_car_motion_data[0].m_world_position_x = packet[i] * -1
        elif i == "m_worldPosY":
            packetdata.m_car_motion_data[0].m_world_position_z = packet[i]
        elif i == "m_worldPosZ":
            packetdata.m_car_motion_data[0].m_world_position_y = packet[i]
        elif i == "worldForwardDirX":
            packetdata.m_car_motion_data[0].m_world_forward_dir_x = packet[i]
        elif i == "worldForwardDirY":
            packetdata.m_car_motion_data[0].m_world_forward_dir_y = packet[i]
        elif i == "worldForwardDirZ":
            packetdata.m_car_motion_data[0].m_world_forward_dir_z = packet[i]
        elif i == "worldRightDirX":
            packetdata.m_car_motion_data[0].m_world_right_dir_x = packet[i]
        elif i == "worldRightDirY":
            packetdata.m_car_motion_data[0].m_world_right_dir_y = packet[i]
        elif i == "worldRightDirZ":
            packetdata.m_car_motion_data[0].m_world_right_dir_z = packet[i]
        elif i == "m_yaw":
            packetdata.m_car_motion_data[0].m_yaw = packet[i]
        elif i == "m_pitch":
            packetdata.m_car_motion_data[0].m_pitch = packet[i]
        elif i == "m_roll":
            packetdata.m_car_motion_data[0].m_roll = packet[i]
        elif i == "m_front_wheels_angle":
            packetdata.m_front_wheels_angle = packet[i]
    packetdata.m_header.m_packet_format = version
    packetdata.m_header.m_packet_version = 1
    packetdata.m_header.m_packet_id = 0
    write_pickle(m_timestamp,'motion',packetdata)
    # print(packetdata)

def create_telemetrydata_packet(packet,version):
    packetclass = f1sim.loadclass("telemetry_f1_"+str(version)+".packets.PacketCarTelemetryData")
    emptydata = bytes(packetclass.size())
    packetdata = packetclass.from_buffer_copy(emptydata)
    m_timestamp = None
    m_gamehost = None
    for i in packet:
        # print(i,packet[i])
        if i == "m_timestamp":
            m_timestamp = packet[i]
        elif i == "m_gamehost":
            m_gamehost = packet[i]
        elif i == "m_session":
            packetdata.m_header.m_session_uid = packet[i]
        elif i == "m_frame":
            packetdata.m_header.m_frame_identifier = packet[i]
        elif i == "m_speed":
            packetdata.m_car_telemetry_data[0].m_speed = packet[i]
        elif i == "m_throttle":
            packetdata.m_car_telemetry_data[0].m_throttle = packet[i]
        elif i == "m_brake":
            packetdata.m_car_telemetry_data[0].m_brake = packet[i]
        elif i == "m_gear":
            packetdata.m_car_telemetry_data[0].m_gear = packet[i]
        elif i == "m_drs":
            packetdata.m_car_telemetry_data[0].m_drs = packet[i]
        elif i == "m_steer":
            packetdata.m_car_telemetry_data[0].m_steer = packet[i]
        elif i == "m_engineRPM":
            packetdata.m_car_telemetry_data[0].m_engine_rpm = packet[i]
        elif i == "m_engine_temperature":
            packetdata.m_car_telemetry_data[0].m_engine_temperature = packet[i]
        elif i == "m_brakes_temperature":
            packetdata.m_car_telemetry_data[0].m_brakes_temperature[0] = packet[i][0]
            packetdata.m_car_telemetry_data[0].m_brakes_temperature[1] = packet[i][1]
            packetdata.m_car_telemetry_data[0].m_brakes_temperature[2] = packet[i][2]
            packetdata.m_car_telemetry_data[0].m_brakes_temperature[3] = packet[i][3]
        elif i == "m_tyres_surface_temperature":
            packetdata.m_car_telemetry_data[0].m_tyres_surface_temperature[0] = packet[i][0]
            packetdata.m_car_telemetry_data[0].m_tyres_surface_temperature[1] = packet[i][1]
            packetdata.m_car_telemetry_data[0].m_tyres_surface_temperature[2] = packet[i][2]
            packetdata.m_car_telemetry_data[0].m_tyres_surface_temperature[3] = packet[i][3]
        elif i == "m_tyres_inner_temperature":
            packetdata.m_car_telemetry_data[0].m_tyres_inner_temperature[0] = packet[i][0]
            packetdata.m_car_telemetry_data[0].m_tyres_inner_temperature[1] = packet[i][1]
            packetdata.m_car_telemetry_data[0].m_tyres_inner_temperature[2] = packet[i][2]
            packetdata.m_car_telemetry_data[0].m_tyres_inner_temperature[3] = packet[i][3]
        elif i == "m_tyres_pressure":
            packetdata.m_car_telemetry_data[0].m_tyres_pressure[0] = packet[i][0]
            packetdata.m_car_telemetry_data[0].m_tyres_pressure[1] = packet[i][1]
            packetdata.m_car_telemetry_data[0].m_tyres_pressure[2] = packet[i][2]
            packetdata.m_car_telemetry_data[0].m_tyres_pressure[3] = packet[i][3]
    packetdata.m_header.m_packet_format = version
    packetdata.m_header.m_packet_version = 1
    packetdata.m_header.m_packet_id = 6
    write_pickle(m_timestamp,'telemetry',packetdata)
    # print(packetdata)

def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if default_type == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)

def main():
    # data = bytes(48)
    for i in HEADER_FIELD_TO_PACKET_TYPE:
        print(i,HEADER_FIELD_TO_PACKET_TYPE[i].size())

    if sys.platform == 'win32':
        cx_Oracle.init_oracle_client(lib_dir=os.getenv('ORACLE_HOME'))

    dbusername = "anziot"
    dbpassword = "6#VCJcR0mB!z9lb"
    dburl = "fortatp_low"
    # dbusername = "simdev"
    # dbpassword = "W3lc0m3DEV123"
    # dburl = "f1simtp_low"
    poolsize = 1
    session_uid = None
    if len(sys.argv) >= 2:
        session_uid = sys.argv[1]
    logging.debug(os.getenv("TNS_ADMIN"))
    logging.debug(dburl)
    logging.debug(dbusername)
    logging.debug(dbpassword)
    logging.debug(poolsize)
    logging.info("Sending to " + dbusername+"@"+dburl);
    pool = cx_Oracle.SessionPool(dbusername, dbpassword, dburl, min=poolsize, max=poolsize, increment=1, threaded=True,getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT)
    pool.ping_interval = 120
    pool.timeout = 600
    logging.info('Connection successful.')

    connection = pool.acquire()
    connection.autocommit = True
    # connection.outputtypehandler = output_type_handler
    sessioncursor = cx_Oracle.Cursor(connection)
    sessionstmt = 'select JSON_OBJECT(DATA) from "F1SIM-SESSION" l'
    if session_uid != None:
        sessionstmt = sessionstmt + ' where l."DATA".m_session = '+str(session_uid)
    sessioncursor.execute(sessionstmt)
    while True:
        sessiondata = sessioncursor.fetchone()
        if sessiondata is None:
            break
        # print(sessiondata)
        sessionpacket = json.loads(sessiondata[0])["DATA"]
        # print("loading data")
        # print(packet["m_session"])
        # print(sessionpacket)
        version = create_sessiondata_packet(sessionpacket)
        lapcursor = cx_Oracle.Cursor(connection)
        lapcursor.execute('select JSON_OBJECT(DATA) from "F1SIM-LAPDATA" l WHERE l."DATA".m_session = '+str(sessionpacket["m_session"]))
        while True:
            lapdata = lapcursor.fetchone()
            if lapdata is None:
                break
            lappacket = json.loads(lapdata[0])["DATA"]
            # print("loading data")
            # print(packet["m_session"])
            # print(lappacket)
            create_lapdata_packet(lappacket,version)
        motioncursor = cx_Oracle.Cursor(connection)
        motioncursor.execute('select JSON_OBJECT(DATA) from "F1SIM-MOTION" l WHERE l."DATA".m_session = '+str(sessionpacket["m_session"]))
        while True:
            motiondata = motioncursor.fetchone()
            if motiondata is None:
                break
            motionpacket = json.loads(motiondata[0])["DATA"]
            # print("loading data")
            # print(packet["m_session"])
            # if str(packet["m_session"]) == "18303027189558209429":
            # print(motionpacket)
            create_motiondata_packet(motionpacket,version)
        telemetrycursor = cx_Oracle.Cursor(connection)
        telemetrycursor.execute('select JSON_OBJECT(DATA) from "F1SIM-TELEMETRY" l WHERE l."DATA".m_session = '+str(sessionpacket["m_session"]))
        while True:
            telemetrydata = telemetrycursor.fetchone()
            if telemetrydata is None:
                break
            telemetrypacket = json.loads(telemetrydata[0])["DATA"]
            # print("loading data")
            # print(packet["m_session"])
            # print(telemetrypacket)
            create_telemetrydata_packet(telemetrypacket,version)
    pool.release(connection)
    pool.close()
    logging.info('Connection pool closed.')


if __name__ == '__main__':
    main()
