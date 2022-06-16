# https://www.sciosense.com/wp-content/uploads/documents/SC-001224-DS-7-ENS160-Datasheet.pdf
# https://github.com/DFRobot/DFRobot_ENS160
# Peter Johnston at Core Electronics June 2022

from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_I2C_ADDRESS = 0x52

_REG_PART_ID       = 0x00
_REG_OPMODE        = 0x10
_REG_CONFIG        = 0x11
_REG_COMMAND       = 0x12
_REG_TEMP_IN       = 0x13
_REG_RH_IN         = 0x15
_REG_DEVICE_STATUS = 0x20
_REG_DATA_AQI      = 0x21
_REG_DATA_TVOC     = 0x22
_REG_DATA_ECO2     = 0x24
_REG_DATA_T        = 0x30
_REG_DATA_RH       = 0x32
_REG_DATA_MISR     = 0x38
_REG_GPR_WRITE     = 0x40
_REG_GPR_READ      = 0x48

_BIT_CONFIG_INTEN   = 0
_BIT_CONFIG_INTDAT  = 1
_BIT_CONFIG_INTGPR  = 3
_BIT_CONFIG_INT_CFG = 5
_BIT_CONFIG_INTPOL  = 6

_BIT_DEVICE_STATUS_NEWGPR        = 0
_BIT_DEVICE_STATUS_NEWDAT        = 1
_BIT_DEVICE_STATUS_VALIDITY_FLAG = 2
_BIT_DEVICE_STATUS_STATER        = 6
_BIT_DEVICE_STATUS_STATAS        = 7

_VAL_PART_ID           = 0x160
_VAL_OPMODE_DEEP_SLEEP = 0x00
_VAL_OPMODE_IDLE       = 0x01
_VAL_OPMODE_STANDARD   = 0x02
_VAL_OPMODE_RESET      = 0xF0

def _readBit(x, n):
    return x & 1 << n != 0

def _readCrumb(x, n):
    return _readBit(x, n) + _readBit(x, (n+1))^2

def _readTribit(x, n):
    return _readBit(x, n) + _readBit(x, (n+1))^2 + _readBit(x, (n+2))^3

def _setBit(x, n):
    return x | (1 << n)

def _clearBit(x, n):
    return x & ~(1 << n)

def _writeBit(x, n, b):
    if b == 0:
        return _clearBit(x, n)
    else:
        return _setBit(x, n)

class PiicoDev_ENS160(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_I2C_ADDRESS, intdat=False, intgpr=False, int_cfg=0, intpol=0, temperature=25, humidity=70):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.address = address
        config = 0x00
        if intdat or intgpr:
            config = _setBit(config, _BIT_CONFIG_INTEN)
            config = _writeBit(config, _BIT_CONFIG_INTDAT, intdat)
            config = _writeBit(config, _BIT_CONFIG_INTGPR, intgpr)
        config = _writeBit(config, _BIT_CONFIG_INT_CFG, int_cfg)
        config = _writeBit(config, _BIT_CONFIG_INTPOL, intpol)
        self.config = config
        try:
            part_id = self._readInt(_REG_PART_ID, 2)
            print('part_id: ' + str(part_id))
            if part_id != _VAL_PART_ID:
                print('Device is not PiicoDev ENS160')
                raise SystemExit
            self._writeInt(_REG_OPMODE, _VAL_OPMODE_STANDARD, 1)
            #self._write(_REG_OPMODE, bytes(_VAL_OPMODE_STANDARD))
            sleep_ms(20)
            print('written opmode standard')
            opmode = self._readInt(_REG_OPMODE, 1)
            print('op mode: ' + str(opmode))
            sleep_ms(20)
            self._writeInt(_REG_CONFIG, self.config, 1)
            print('written config register')
            self.setTemperature(temperature)
            print('set the temperature')
            self.setHumidity(humidity)
            self.getDeviceStatus()
        except Exception as e:
            print(i2c_err_str.format(self.address))
            raise e
        
    def _read(self, register, length):
        try:
            return self.i2c.readfrom_mem(self.address, register, length)
        except:
            print(i2c_err_str.format(self.address))
            return None
        
    def _write(self, register, data):
        try:
            return self.i2c.writeto_mem(self.address, register, data)
        except:
            print(i2c_err_str.format(self.address))
            return None
        
    def _readInt(self, register, length):
        return int.from_bytes(self._read(register, length),'little')

    def _writeInt(self, register, integer, length):
        return self._write(register, int.to_bytes(integer,length,'little'))
        
    def getDeviceStatus(self):
        device_status = int.from_bytes(self._read(_REG_DEVICE_STATUS, 1),'little')
        print('device_status: ' + str(device_status))
        self.statas = _readBit(device_status, _BIT_DEVICE_STATUS_STATAS)
        self.stater = _readBit(device_status, _BIT_DEVICE_STATUS_STATER)
        self.validity_flag = _readCrumb(device_status, _BIT_DEVICE_STATUS_VALIDITY_FLAG)
        self.newdat = _readBit(device_status, _BIT_DEVICE_STATUS_NEWDAT)
        self.newgpr = _readBit(device_status, _BIT_DEVICE_STATUS_NEWGPR)
        
    def setTemperature(self, temperature):
        kelvin = int(temperature + 273.15)
        buf = [0x00, 0x00]
        buf[0] = (kelvin * 64) & 0xFF
        buf[1] = ((kelvin *64) & 0xFF00) >> 8
        #self._write(_REG_TEMP_IN, bytes(buf))
        self._writeInt(_REG_TEMP_IN, kelvin * 64, 2)
            
    def setHumidity(self, humidity):
        buf = [0,0]
        buf[0] = ((humidity * 512) & 0xFF)
        buf[1] = ((humidity * 512) & 0xFF00) >> 8
#        self._write(_REG_RH_IN, bytes(buf))
        self._writeInt(_REG_RH_IN, humidity * 512, 2)
        
    def getTemperature(self):
        kelvin = self._readInt(_REG_DATA_T, 2) / 64
        return kelvin - 273.15
        
    def getHumidity(self):
        return self._readInt(_REG_DATA_RH, 2) / 512
    
    def readAQI(self):
        aqi = _readTribit(self._readInt(_REG_DATA_AQI, 2), 0)
        if aqi is not None:
            return aqi
        else:
            return aqi
    
    def readTVOC(self):
        tvoc = self._readInt(_REG_DATA_TVOC, 2)
        if tvoc is not None:
            return tvoc
        else:
            return tvoc
        
    def readECO2(self):
        eco2 = self._readInt(_REG_DATA_ECO2, 2)
        if eco2 is not None:
            return eco2
        else:
            return eco2
        