

# https://www.raspberrypi.com/documentation/computers/os.html#vcgencmd

#Example to play audio
#omxplayer example.mp3

# SoC Temp
#vcgencmd measure_temp
#PMIC temp
#vcgencmd measure_temp pmic

#Returns the throttled state of the system
#vcgencmd get_throttled
#0
# 0x1
# Under-voltage detected
# 1
# 0x2
# Arm frequency capped
# 2
# 0x4
# Currently throttled
# 3
# 0x8
# Soft temperature limit active
# 16
# 0x10000
# Under-voltage has occurred
# 17
# 0x20000
# Arm frequency capping has occurred
# 18
# 0x40000
# Throttling has occurred
# 19
# 0x80000
# Soft temperature limit has occurred


# measure_clock [clock]
#
# This returns the current frequency of the specified clock. The options are:
#
# clock	Description
# arm
# ARM core(s)
# core
# GPU core
# H264
# H.264 block
# isp
# Image Sensor Pipeline
# v3d
# 3D block
# uart
# UART
# pwm
# PWM block (analogue audio output)
# emmc
# SD card interface
# pixel
# Pixel valves
# vec
# Analogue video encoder
# hdmi
# HDMI
# dpi
# Display Parallel Interface


# measure_volts [block]
#
# Displays the current voltages used by the specific block.
#
# block	Description
# core
# VC4 core voltage
# sdram_c
# SDRAM Core Voltage
# sdram_i
# SDRAM I/O voltage
# sdram_p
# SDRAM Phy Voltage



# get_mem type
#
# Reports on the amount of memory addressable by the ARM and the GPU. To show the amount of ARM-addressable memory use vcgencmd get_mem arm; to show the amount of GPU-addressable memory use vcgencmd get_mem gpu. Note that on devices with more than 1GB of memory the arm parameter will always return 1GB minus the gpu memory value, since the GPU firmware is only aware of the first 1GB of memory. To get an accurate report of the total memory on the device, see the total_mem configuration item - see get_config section above.



# pip install psutil
# pip install gpiozero

# https://amalgjose.com/2020/04/27/simple-python-program-to-get-the-system-status-of-a-raspberry-pi/

import psutil
# Get cpu statistics
cpu = str(psutil.cpu_percent()) + '%'

# Calculate memory information
memory = psutil.virtual_memory()

# Convert Bytes to MB (Bytes -> KB -> MB)
available = round(memory.available/1024.0/1024.0,1)
total = round(memory.total/1024.0/1024.0,1)
mem_info = str(available) + 'MB free / ' + str(total) + 'MB total ( ' + str(memory.percent) + '% )'

# Calculate disk information
disk = psutil.disk_usage('/')

# Convert Bytes to GB (Bytes -> KB -> MB -> GB)
free = round(disk.free/1024.0/1024.0/1024.0,1)
total = round(disk.total/1024.0/1024.0/1024.0,1)
disk_info = str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )'
print("CPU Info -> ", cpu)
print("Memory Info ->", mem_info)
print("Disk Info ->", disk_info)



#!/usr/bin/python3
import psutil
from gpiozero import CPUTemperature
import socket
import re, uuid

MAX_MEMORY = 1024.0

def get_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

# Get cpu statistics
cpu = str(psutil.cpu_percent()) + '%'

# Calculate memory information
memory = psutil.virtual_memory()

# Convert Bytes to MB (Bytes -> KB -> MB)
memory_available = round(memory.available/MAX_MEMORY/MAX_MEMORY, 1)
memory_total = round(memory.total/MAX_MEMORY/MAX_MEMORY, 1)
memory_percent = str(memory.percent) + '%'

# Calculate disk information
disk = psutil.disk_usage('/')

# Convert Bytes to GB (Bytes -> KB -> MB -> GB)
disk_free = round(disk.free/MAX_MEMORY/MAX_MEMORY/MAX_MEMORY, 1)
disk_total = round(disk.total/MAX_MEMORY/MAX_MEMORY/MAX_MEMORY, 1)
disk_percent = str(disk.percent) + '%'

# Temperature
# $vcgencmd measure_temp
# $vcgencmd measure_temp pmic?
temperature_info = CPUTemperature().temperature
temperature = "{:.4f}'C'".format(temperature_info)

# Network
ip_address = get_ip()
mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

# Output Info
print("CPU Info -> ", cpu)
#print("Memory -> ", memory)
print("Memory Free -> ", memory_available)
print("Memory Total -> ", memory_total)
print("Memory Percentage -> ", memory_percent)
#print("Disk Info -> ", disk)
print("Disk Free -> ", disk_free)
print("Disk Total -> ", disk_total)
print("Disk Percentage -> ", disk_percent)
print("CPU Temperature -> ", temperature)
print("IP Address -> ", ip_address)
print("MAC Address -> ", mac_address)
