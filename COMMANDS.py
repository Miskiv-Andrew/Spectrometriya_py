class Const:
    MAX_ERROR = 3
    WAIT_TIME = 1000
    READ_PAUSE = 0.1  #Const.READ_PAUSE
    NUM_ITERATION = 21 #10 # Кол-во итераций по "наполнению" парами импульс-время 1 секунды
    GLOB_BUFF_SIZE = 1200000 


class Command: 
    def __init__(self, name: str, data: bytes, length: int): 
        self.name = name
        self.data = data 
        self.length = length


class DeviceCommands():            
    COMMAND_RAD_DOSE              =  Command("RAD_DOSE",               bytes([0x55, 0xAA, 0x70, 0x01, 0x00 ]), 12)      
    COMMAND_SER_NUM               =  Command("SER_NUM",                bytes([0x55, 0xAA, 0x70, 0x01, 0x05 ]), 11)   
    COMMAND_RAD_INTENS            =  Command("RAD_INTENS",             bytes([0x55, 0xAA, 0x70, 0x01, 0x04 ]), 10) 
    COMMAND_TEMP                  =  Command("TEMP",                   bytes([0x55, 0xAA, 0x70, 0x01, 0x08]), 8) 
    COMMAND_TOGGLE_SIMPLE_SPECTRE =  Command("TOGGLE_SIMPLE_SPECTRE",  bytes([0x55, 0xAA, 0x70, 0x01, 0x8B, 0x09, 0x8C, 0x01]), 2098)
    COMMAND_TOGGLE_TIME_SPECTRE   =  Command("TOGGLE_TIME_SPECTRE",    bytes([0x55, 0xAA, 0x70, 0x01, 0x4B, 0x09, 0x8C, 0x01]), 9020)
 





