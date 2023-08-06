# -----------------------------------------------------------------------------
# - File              usbswsdk.py
# - Owner             Zhengkun Li
# - Version           1.1
# - Date              09.06.2021
# - Classification    Python SDK
# - Brief             Python SDK for ZD USB Switch
# - History        
#       2021.06.09    Initial version.                   Zhengkun Li
#       2021.09.27    Add set_relay/set_power commands.  Yu-Ling Xie
# ----------------------------------------------------------------------------- 

import serial
import serial.tools.list_ports as port_list
import time
import colorama
colorama.init()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
################################################################################
# Description : Check serial port                                              #
# Argument: None                                                               #                             
# Returns: The list of serial COM ports in use :list                           #    
################################################################################  
def detect_comports():
    com_ports_details = list(port_list.comports())
    com_ports = []
    for p in com_ports_details:
        print(f"{bcolors.OKGREEN}{p}{bcolors.ENDC}")
        com_ports.append(str(p).split(" ")[0])
    
    return com_ports
################################################################################
# Description : Get Current Version Information                                #
# Argument: dev_port: str                                                      #                             
# Returns: None                                                                #    
################################################################################  
def get_version(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<GET_SW_VERSION{}>")
    serialString = ""  # Used to hold data coming over UART
    strData = []
    res = [None]

    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res[0]
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            
            # return ok
            if '[GET_SW_VERSION{v' in serialString:
                strData = serialString.strip().lstrip('[GET_SW_VERSION{').rstrip('}]')
                res = strData.split(' ')

            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Reboot System                                                  #
# Argument: dev_port: str                                                      #                             
# Returns: None                                                                #    
################################################################################
def reboot_sys(dev_port: str):
    time_start=time.time() 
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<REBOOT_SYS{}>")
    serialString = ""  # Used to hold data coming over UART

    while 1 :
        time_end=time.time()
        if (time_end-time_start)>10:
            return  
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
           
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass
################################################################################
# Description : Save Configuration into Flash                                  #
# Argument: dev_port: str                                                      #                             
# Returns: Save status: bool                                                   # 
################################################################################     
def save_config(dev_port: str):
    time_start=time.time() 
    res = False
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<SAVE_CONFIG{}>")
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[SAVE_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass

################################################################################
# Description : Clear Configuration in Flash                                   #
# After the configuration has been modified, following command could reset all #
# configuration to initial                                                     #  
# Argument: dev_port: str                                                      #                             
# Returns: Clear status:bool                                                   #    
################################################################################   
def clr_config(dev_port: str):
    time_start=time.time() 
    res = False
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<CLEAR_CONFIG{}>")
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>2:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[CLEAR_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass


################################################################################
# Description : Display Current Configuration in Ram                           #
# Argument: dev_port: str                                                      #                             
# Returns: Display result: bool                                                #    
################################################################################
def disp_config(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write(b"<DISP_CONFIG{}>")
    res = False
    serialString = ""  # Used to hold data coming over UART
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[DISP_CONFIG{ok}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass
################################################################################
# Description : Set Enable Host Port                                           #
# Argument: dev_port: str, 1~4 : int                                           #                             
# Returns: Set Enable Host Port result: bool                                   #    
################################################################################  
def set_host_port(dev_port: str,port_num:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes(f"<SET_HOST_PORT{{{port_num}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>2:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_HOST_PORT{{{port_num}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  

################################################################################
# Description : Get Enable Host Port                                           #
# Argument: dev_port: str                                                      #                             
# Returns:  Currently Enabled Host Port: int                                   #    
################################################################################  
def get_host_port(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes("<GET_HOST_PORT{}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_HOST_PORT{" in serialString:               
                res = serialString.strip('[GET_HOST_PORT{')[0]
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

################################################################################
# Description : Set Enable Device Port                                         #
# Argument: dev_port: str, 1~4 : int                                           #                             
# Returns: Set enable port of Device status: bool                              #    
################################################################################    
def set_dev_port(dev_port: str,port_num:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes(f"<SET_DEVICE_PORT{{{port_num}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>2:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_DEVICE_PORT{{{port_num}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

################################################################################
# Description : Get Enable Device Port                                         #
# Argument: dev_port: str                                                      #                             
# Returns:  Currently Enabled Device Port: int                                 #    
################################################################################  
def get_dev_port(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes("<GET_DEVICE_PORT{}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            
            if "[GET_DEVICE_PORT{" in serialString:               
                res = serialString.lstrip('[GET_DEVICE_PORT{')[0]
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass    
################################################################################
# Description : Set Relay Mask                                                 #
# Argument:dev_port: str, mask: 0x0 – 0xf:int                                  #                             
# Returns:                                                                     #
# Set the Mask to control the Relays, 4bit Mask value, Bit0 to Bit3 stand for  #
# Relay1 to Relay4. : bool                                                     #    
################################################################################ 
def set_relay_mask(dev_port: str,mask:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes(f"<SET_RELAY_MASK{{{hex(mask)}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_RELAY_MASK{{{hex(mask)}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  

################################################################################
# Description : Get Relay Mask                                                 #
# Argument: dev_port: str                                                      #                             
# Returns:                                                                     #
# Get the current Mask of Relays, Bit0 to Bit3 stand for Relay1 to Relay4: int #    
################################################################################ 
def get_relay_mask(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes("<GET_RELAY_MASK{}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_RELAY_MASK{" in serialString:               
                res = int(serialString.strip().lstrip('[GET_RELAY_MASK{').rstrip("}]"),0)
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass    

################################################################################
# Description : Set Power Supply Mask                                          #
# Argument: dev_port: str , 0x0 – 0xf:int                                      #                             
# Description                                                                  #  
# Set the Mask of the Device Ports enable to power supply, Bit0 to Bit3 stand  #
# for Port1 to Port4.                                                          #     
# e.g. <SET_POWER_MASK{0x0}> (Binary:0000), all device port dose not power     #
#           supply, only data exchange .                                       #
#      <SET_POWER_MASK{0xf}> (Binary:1111), all device port can power supply.  #    
################################################################################     
def set_pwr_mask(dev_port: str,mask:int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes(f"<SET_POWER_MASK{{{hex(mask)}}}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if f"[SET_POWER_MASK{{{hex(mask)}}}]" in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 
################################################################################
# Description : Get Power Supply Mask                                          #
# Argument: None                                                               #                             
# Description                                                                  #  
# Get the current Mask of the enable Device Ports to power supply, Bit0 to Bit3#
# stand for Port1 to Port4.                                                    #     
# e.g. <SET_POWER_MASK{0x0}> (Binary:0000), all device port dose not power     #
#           supply, only data exchange .                                       #
#      <SET_POWER_MASK{0xf}> (Binary:1111), all device port can power supply.  #    
################################################################################  
def get_pwr_mask(dev_port: str): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes("<GET_POWER_MASK{}>", encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if "[GET_POWER_MASK{" in serialString:               
                res = int(serialString.strip().lstrip('[GET_POWER_MASK{').rstrip("}]"),0)
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  

################################################################################
# Description : Set Relay                                                      #
# Argument:dev_port: str, relay_port: int, control: int                                       #                             
# Returns:                                                                     #
# Set the control of the specific relay. 0-open, 1-close                       #
# Relay1 to Relay4. : bool                                                     #    
################################################################################ 
def set_relay(dev_port: str,relay_port: int,control: int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes('<SET_RELAY{'+str(relay_port)+','+str(control)+'}>', encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if '[SET_RELAY{'+str(relay_port)+','+str(control)+'}]' in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass  

################################################################################
# Description : Get Relay                                                      #
# Argument: dev_port: str, relay_port: int                                     #                             
# Returns:                                                                     #
# Get the current control of Relay                                             #    
################################################################################ 
def get_relay(dev_port: str,relay_port: int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes('<GET_RELAY{'+str(relay_port)+'}>', encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    data = [0] * 2    
    strData = []    
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")

            # Print the contents of the serial data
            print(serialString)

            if "[GET_RELAY{" in serialString:
                res = serialString.strip().lstrip('[GET_RELAY{').rstrip('}]')
                strData = res.split(',')
                data[0] = int(strData[0])
                data[1] = int(strData[1])
                return data                
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass    

################################################################################
# Description : Set Power Supply                                               #
# Argument: dev_port: str , power_device: int, control: int                    #                             
# Description                                                                  #  
# Set the Device Port enable to power supply.                                  #
#     control=0: power off; control=1: power on                                #
# e.g. <SET_POWER{1, 0}> , device1 is set to power down.                       #
################################################################################     
def set_pwr(dev_port: str,power_device: int,control: int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes('<SET_POWER{'+str(power_device)+','+str(control)+'}>', encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = False
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:
            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            if '[SET_POWER{'+str(power_device)+','+str(control)+'}]' in serialString:
                res =  True
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

################################################################################
# Description : Get Power Supply Status                                        #
# Argument: power_device: int                                                  #                             
# Description                                                                  #  
# Get the current control status of the Device Port                            #
################################################################################  
def get_pwr(dev_port: str,power_device: int): 
    time_start=time.time()  
    serialPort = serial.Serial(port=dev_port, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.write( bytes('<GET_POWER{'+str(power_device)+'}>', encoding = "utf8"))
    serialString = ""  # Used to hold data coming over UART
    res = None
    data = [0] * 2    
    strData = []
    while 1 :
        time_end=time.time()
        if (time_end-time_start)>1:
            return res
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode("Ascii")
            # Print the contents of the serial data
            print(serialString)

            if "[GET_POWER{" in serialString:
                res = serialString.strip().lstrip('[GET_POWER{').rstrip('}]')
                strData = res.split(',')
                data[0] = int(strData[0])
                data[1] = int(strData[1])
                return data
            # Print the contents of the serial data
            try:
                print(serialString)
            except:
                pass 

