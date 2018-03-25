#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################
#Written by Yi Herng Ong
#ME 599 Project Script 1 - Python Controller
#This code is partially taken from code examples by Dynamixel SDK
#Cited Sources: 
#Leon(2017)read_write.py(protocol 1.0)[Source Code].https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/master/python/protocol1_0/read_write.py
#Leon(2017)dynamixel_functions.py[Source Code].https://github.com/ROBOTIS-GIT/DynamixelSDK/blob/master/python/dynamixel_functions_py/dynamixel_functions.py
#############################################################

import os
import serial


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('../dynamixel_functions_py')             # Path setting

import dynamixel_functions as dynamixel

###########################################################
# Control Table Address
ADDR_MX_TORQUE_ENABLE       = 24                            # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION       = 30
ADDR_MX_PRESENT_POSITION    = 36

# Protocol version
PROTOCOL_VERSION            = 1                             # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                             # Dynamixel ID: 1
BAUDRATE                    = 57600
DEVICENAME                  = "/dev/ttyUSB0"#.encode('utf-8')# Check which port is being used on your controller
                                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                             # Value for enabling the torque
TORQUE_DISABLE              = 0                             # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100                           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000                          # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD_FINGER = 10                            # Dynamixel moving status threshold for finger 
DXL_MOVING_STATUS_THRESHOLD_SPREAD = 50                            # Dynamixel moving status threshold for spread

ESC_ASCII_VALUE             = 0x1b

COMM_SUCCESS                = 0                             # Communication Success result value
COMM_TX_FAIL                = -1001                         # Communication Tx Failed

##########################################################

#Class to setup device for Openhand (Leon,2017)
class SetUp_():
    def __init__(self, port_num):
        global BAUDRATE
        if port_num == None:
            raise ValueError
        self.baudrate = BAUDRATE
        self.port_num = port_num

    #Open USB port that connected to Openhand
    def Open_port(self):
        if dynamixel.openPort(self.port_num):
            return True
        else:
            print("Failed to open the port!")
            print("Press any key to terminate...")
            getch()
            quit()
            return False
    #Set Baudrate for Openhand (for DynamixelSDK servo MX 28 is 57600)
    def Set_baudrate(self):
        if dynamixel.setBaudRate(self.port_num,self.baudrate):
            print("Succeeded to change baudrate!")
        else:
            print("Failed to change the baudrate!")
            print("Press any key to terminate...")
            getch()
            quit()
        return None

    #Close USB port
    def Close_port(self):
        dynamixel.closePort(port_num)
        return None

#Class to actuate Openhand finger that attached to DynamixelSDK servo (Leon,2017)
class Dynamixel_servo():
    def __init__(self, port_num, pro_ver, ID = 1):
        global COMM_SUCCESS, COMM_TX_FAIL, ADDR_MX_PRESENT_POSITION, ADDR_MX_GOAL_POSITION, ADDR_MX_TORQUE_ENABLE
        self.ID = ID
        self.port_num = port_num
        self.pro_ver = pro_ver
        self.addr_torque = ADDR_MX_TORQUE_ENABLE
        self.addr_present = ADDR_MX_PRESENT_POSITION
        self.addr_goal = ADDR_MX_GOAL_POSITION
        self.COMM_SUCCESS = COMM_SUCCESS
        self.COMM_TX_FAIL = COMM_TX_FAIL
        self.dxl_comm_result = COMM_TX_FAIL
        self.dxl_error = 0
        self.dxl_present_position = 0

    #Initiate torque for servo (Leon, 2017)
    def EnableTorque(self):
        dynamixel.write1ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_torque, 1)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            print(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))
        else:
            print("Dynamixel has been successfully connected")
        return None        

    #Move servo and finger to goal position (Leon, 2017)
    def Move(self,goalpos):
        self.goalpos = int(goalpos)
        # Write goal position
        dynamixel.write2ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_goal, self.goalpos)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            print(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))
        return None

    #Print current position of finger(Leon,2017)
    def PresentPos_finger(self):
        #Print current pos with goalpos
        global DXL_MOVING_STATUS_THRESHOLD
        #Read present position
        self.dxl_present_position = dynamixel.read2ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_present)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            return(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            return(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (self.ID, self.goalpos, self.dxl_present_position))

        if not (abs(self.goalpos - self.dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD_FINGER):
           return True
        return False

    #Print current position of spread (Leon, 2017)
    def PresentPos_spread(self):
        #Print current pos with goalpos
        global DXL_MOVING_STATUS_THRESHOLD
        #Read present position
        self.dxl_present_position = dynamixel.read2ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_present)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            return(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            return(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (self.ID, self.goalpos, self.dxl_present_position))

        if not (abs(self.goalpos - self.dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD_SPREAD):
           return True
        return False

    #Print current position of finger without requiring goal pos (Leon, 2017)
    def PresentPos_1(self):
        #Print current pos without goalpos
        global DXL_MOVING_STATUS_THRESHOLD
        #Read present position
        self.dxl_present_position = dynamixel.read2ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_present)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            return(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            return(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))
        print("[ID:%03d] PresPos:%03d" % (self.ID, self.dxl_present_position))
        return None

    #Close servo torque (Leon, 2017)
    def DisableTorque(self):
        # Disable Dynamixel Torque
        dynamixel.write1ByteTxRx(self.port_num, self.pro_ver, self.ID, self.addr_torque, 0)
        self.dxl_comm_result = dynamixel.getLastTxRxResult(self.port_num, self.pro_ver)
        self.dxl_error = dynamixel.getLastRxPacketError(self.port_num, self.pro_ver)
        if self.dxl_comm_result != self.COMM_SUCCESS:
            print(dynamixel.getTxRxResult(self.pro_ver, self.dxl_comm_result))
        elif self.dxl_error != 0:
            print(dynamixel.getRxPacketError(self.pro_ver, self.dxl_error))
        return None

    #Reset finger position 
    def Finger_Reset(self):
        #Reset to original position
        Move(0)
        return None

    #Reset spread position
    def Spread_Reset(self):
        #Reset spread to zero position
        Move(4095)
        return None

#Class for Arduino Slidy Box
class Slidybox():
    def __init__(self,port_name,baudrate):
        self.port_name = port_name
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port_name, self.baudrate)
        self.val = []
        self.newval = []
        self.fingerscale = 2000 / 2.5
        self.spreadscale = 4095 / 3.14

    #Turn on Slidy Box and read outputs
    def Open_Slidybox(self):
        self.ser.readline()
        return None

    #Store slidy box output into array
    def Read_Slidybox(self):
        self.newval = []
        self.val = self.ser.readline().strip()
        self.val = self.val.split(",")
        for idx, x in enumerate(self.val):
            self.val[idx] = float(x)
        return self.val

    #Map finger goal positions from 0.0 - 2.5 to 0 - 2000
    #Map spread goal positions from 0.0 - 3.14 to 4095 - 0 (It is inversed because of gear mechanisms of Openhand)
    def map(self):
        for idx, x in enumerate(self.val[:-1]):
            self.newval.append(int(x*self.fingerscale))
        self.newval.append(4095 - int(self.val[-1]*self.spreadscale))

        return self.newval        


if __name__ == '__main__':

    #Openhand Configuration
    #finger 1 (blue) = ID 2
    #finger 2 (yellow) = ID 1
    #finger 3 (orange) = ID 4
    #Spread = ID 3    

    # Initialize PortHandler Structs (Leon, 2017) 
    # Set the port path (Leon, 2017)
    port_num = dynamixel.portHandler(DEVICENAME)

    # Initialize PacketHandler Structs (leon, 2017)
    dynamixel.packetHandler()
    
    #Initiate variables for storing servo positions
    status1 = 0
    status2 = 0
    status3 = 0
    status4 = 0

    #Open port
    port = SetUp_(port_num)
    if port.Open_port():
        print("Succeeeded to open port!")
        port.Set_baudrate()

    #Initiate servo ID 1,2,3,4
    ID_1 = Dynamixel_servo(port_num, PROTOCOL_VERSION, 1)
    ID_2 = Dynamixel_servo(port_num, PROTOCOL_VERSION, 2)
    ID_3 = Dynamixel_servo(port_num, PROTOCOL_VERSION, 3)
    ID_4 = Dynamixel_servo(port_num, PROTOCOL_VERSION, 4)

    #Print current position without goal pos
    status1 = ID_1.PresentPos_1()
    status2 = ID_2.PresentPos_1()
    status3 = ID_3.PresentPos_1()
    status4 = ID_4.PresentPos_1()

    #Initiate torque for each servo
    ID_1.EnableTorque()
    ID_2.EnableTorque()
    ID_3.EnableTorque()
    ID_4.EnableTorque()

    #Start Arduino Slidy Box
    port = '/dev/ttyACM0'
    b = 9600
    val = []
    s = Slidybox(port,b)
    s.Open_Slidybox()

    #The controller starts.....
    while 1:
        print("Reading slidy box values.... (or press ESC to quit!)")        

        #Read and print outputs from Arduino Slidy Box
        print 'Arduino Slidy Box Output Values: {0}'.format(s.Read_Slidybox())
        print 'Goal positions after mapping: {0}'.format(s.map())

        #Move servos to goal positions
        ID_1.Move(s.newval[2]) #Yellow
        ID_2.Move(s.newval[0]) #Blue
        ID_3.Move(s.newval[3]) #Spread
        ID_4.Move(s.newval[1]) #Orange

        #Print current finger and spread position to see if they meet corresponding goal postion
        while 1:
            status1 = ID_1.PresentPos_finger()
            status2 = ID_2.PresentPos_finger()
            status3 = ID_3.PresentPos_spread()
            status4 = ID_4.PresentPos_finger()

            #if actual position of each servo is less than 10 (finger) or 50 (spread), stop moving, otherwise keep moving
            if status1 or status2 or status3 or status4:   
                break

    #Close each servo torque
    ID_1.DisableTorque()
    ID_2.DisableTorque()
    ID_3.DisableTorque()
    ID_4.DisableTorque()
    
    #Close USB port for Openhand
    port.Close_port()



