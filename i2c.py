import smbus
import time

class ard_i2c:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        # Slave Address 1
        self.address = 0x04
        # Slave Address 2
        self.address_2 = 0x05

    def writeArduino(self, value):
        print(value)
        data_list = list(value)
        for i in data_list:
            self.bus.write_byte(self.address, int(ord(i)))
            self.bus.write_byte(self.address_2, int(ord(i)))
            time.sleep(.1)
        return -1


