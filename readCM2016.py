#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
import serial

SERIAL = "/dev/cu.SLAB_USBtoUART"
 
# Open serial device for reading, it is 19200 baud, 8N1
ser = serial.Serial(SERIAL, 19200)

# supported chemicals, the 9V blocks (Slot A and B) are always NiMH!
CHEM = {
    0: 'NiMH',
    1: 'NiZn'
}

# status of the slot
ACTIVE = {
    0: 'Empty',
    1: 'Active',
}

# Selected program
PROGRAM = {
    0: "Idle",
    1: "Charge",
    2: "Discharge",
    3: "Check",
    4: "Cycle",
    5: "Alive",
    6: "No Param",
    7: "Trickle",
    8: "Waiting",
    9: "Error",
    10: "Ready",
}

# actual mode
MODES = {
    0: "---",
    1: "Charge",
    2: "Discharge",
    3: "Ready",
    4: "Ready",
    5: "Waiting",
    6: "Error",
}

# convert minutes into an hour:minutes string
def timeStr(minutes):
    return '%2.2d:%-2.2d' % (minutes / 60, minutes % 60)

# the 9V slots are named A and B, while the 1.5V slots are 1..4
def slotStr(slot):
    if slot==5:
        return 'A'
    elif slot==6:
        return 'B'
    else:
        return str(slot)

while True:
    # make sure that are no old bytes left in the input buffer
    ser.reset_input_buffer()

    # FYI: the devices sends one package per second

    # each packet starts with 7 bytes, which are the name of the device
    header = ser.read(7)
    if header != 'CM2016 ': # Charge Master 2016 detected?
        continue

    # the next 10 bytes are global data for all slots or the device
    header = ser.read(10)
    print 'VERSION=%d.%d CHEM=%s OVERTEMP_FLAG=%d TEMP_START=%d TEMP_ACT=%d ACTION_CNTR=%d' % ( ord(header[0]),ord(header[1]),CHEM[ord(header[2])],ord(header[3]),struct.unpack(">h", header[4:6])[0],struct.unpack(">h", header[6:8])[0],struct.unpack(">h", header[8:10])[0])

    # the CM2016 has 6 slots, each is 18 bytes of data
    for slot in range(1,7):
        slotData = ser.read(18)
        print 'Slot S%s : %s/%s/%s/?%d? Time=%s Voltage=%.3fV Current=%.3fA CCAP=%.3fmAh DCAP=%.3fmAh' % (slotStr(slot),ACTIVE[ord(slotData[0])],PROGRAM[ord(slotData[1])],MODES[ord(slotData[2])],ord(slotData[3]),timeStr(struct.unpack("<h", slotData[4:6])[0]),struct.unpack("<h", slotData[6:8])[0] / 1000.0,struct.unpack("<h", slotData[8:10])[0] / 1000.0,struct.unpack("<i", slotData[10:14])[0] / 100.0,struct.unpack("<i", slotData[14:18])[0] / 100.0)

    # and a 16 byte CRC follows
    crc = ser.read(2)
    # the way the CRC16 is calculated is unknown to me, it either is a very uncommon one or it is initialized in a different way. The Visual Basic software from Conrad doesn't check for it, it only tests the header
    print
