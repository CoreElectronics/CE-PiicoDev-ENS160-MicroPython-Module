# https://www.sciosense.com/wp-content/uploads/documents/SC-001224-DS-7-ENS160-Datasheet.pdf
# https://github.com/DFRobot/DFRobot_ENS160
# Peter Johnston at Core Electronics June 2022

from PiicoDev_Unified import *
from ucollections import namedtuple
from ustruct import unpack

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

AQI_Tuple = namedtuple("air quality index", ("value", "rating"))
ECO2_Tuple = namedtuple("equivelent carbon dioxide", ("value", "rating"))


def _read_bit(x, n):
    return x & 1 << n != 0

def _read_crumb(x, n):
    return _read_bit(x, n) + _read_bit(x, (n+1))*2

def _read_tribit(x, n):
    return _read_bit(x, n) + _read_bit(x, (n+1))*2 + _read_bit(x, (n+2))*4

def _set_bit(x, n):
    return x | (1 << n)

def _clear_bit(x, n):
    return x & ~(1 << n)

def _write_bit(x, n, b):
    if b == 0:
        return _clear_bit(x, n)
    else:
        return _set_bit(x, n)

class PiicoDev_ENS160(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_I2C_ADDRESS, address_switch=None, asw=None, intdat=False, intgpr=False, int_cfg=0, intpol=0, temperature=25, humidity=70):
        if address_switch == 0 or asw == 0: self.address = _I2C_ADDRESS
        elif address_switch == 1 or asw == 1: self.address = _I2C_ADDRESS - 1
        else: self.address = address
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        config = 0x00
        if intdat or intgpr:
            config = _set_bit(config, _BIT_CONFIG_INTEN)
            config = _write_bit(config, _BIT_CONFIG_INTDAT, intdat)
            config = _write_bit(config, _BIT_CONFIG_INTGPR, intgpr)
        config = _write_bit(config, _BIT_CONFIG_INT_CFG, int_cfg)
        config = _write_bit(config, _BIT_CONFIG_INTPOL, intpol)
        self.config = config
        self._aqi = None
        self._tvoc = None
        self._eco2 = None
        try:
            part_id = self._read_int(_REG_PART_ID, 2)
            print('part_id: ' + str(part_id))
            if part_id != _VAL_PART_ID:
                print('Device is not PiicoDev ENS160')
                raise SystemExit
            self._write_int(_REG_OPMODE, _VAL_OPMODE_STANDARD, 1)
            sleep_ms(20)
            print('written opmode standard')
            opmode = self._read_int(_REG_OPMODE, 1)
            print('OPMODE: ' + str(opmode))
            sleep_ms(20)
            self._write_int(_REG_CONFIG, self.config, 1)
            print('written config register')
            self.temperature = temperature
            print('set the temperature')
            self.humidity = humidity
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
        
    def _read_int(self, register, length):
        return int.from_bytes(self._read(register, length),'little')

    def _write_int(self, register, integer, length):
        return self._write(register, int.to_bytes(integer,length,'little'))

    def _read_data(self):
        if self.status_newdat is True:
            print('----------------------------------------------------------------------------')
            data = _read(self, _REG_DATA_AQI, 5)
            self._aqi, self._tvoc, self._eco2 = unpack('<bhh', data)
    
    @property    
    def humidity(self):
        return self._read_int(_REG_DATA_RH, 2) / 512
    
    @humidity.setter
    def humidity(self, humidity):
        self._write_int(_REG_RH_IN, humidity * 512, 2)
    
    @property
    def temperature(self):
        kelvin = self._read_int(_REG_DATA_T, 2) / 64
        return kelvin - 273.15
    
    @temperature.setter
    def temperature(self, temperature):
        kelvin = temperature + 273.15
        self._write_int(_REG_TEMP_IN, int(kelvin * 64), 2)
    
    @property
    def status(self):
        return int.from_bytes(self._read(_REG_DEVICE_STATUS, 1),'little')
    
    @property
    def status_statas(self):
        return _read_bit(self.status, _BIT_DEVICE_STATUS_STATAS)
    
    @property
    def status_stater(self):
        return _read_bit(self.status, _BIT_DEVICE_STATUS_STATER)
    
    @property
    def status_newdat(self):
        print('new data is being checked')
        temp = _read_bit(self.status, _BIT_DEVICE_STATUS_NEWDAT)
        print('temp: ' + str(temp))
        return temp
    
    @property
    def status_newgpr(self):
        return _read_bit(self.status, _BIT_DEVICE_STATUS_NEWGPR)
    
    @property
    def status_validity_flag(self):
        return _read_crumb(self.status, _BIT_DEVICE_STATUS_VALIDITY_FLAG)
    
    @property
    def status_validity_flag_description(self):
        return ['operating ok', 'warm-up', 'initial start-up', 'no valid output'][self.status_validity_flag]
    
    @property
    def aqi(self):
        self._read_data()
        if self._aqi is not None:
            ratings={1:'excellent', 2:'good', 3:'moderate', 4:'poor', 5:'unhealthy'}
            aqi = _read_tribit(self._aqi, 0)
            return AQI_Tuple(aqi, ratings[aqi])
        else:
            return AQI_Tuple(None, '')

    @property
    def tvoc(self):
        self._read_data()
        if self._tvoc is not None:
            return self._tvoc
        else:
            return None
    
    @property
    def eco2(self):
        self._read_data()
        if self._eco2 is not None:
            eco2 = self._eco2
            rating = 'invalid'
            if eco2 >= 400:
                rating = 'excellent'
            if eco2 > 600:
                rating = 'good'
            if eco2 > 800:
                rating = 'fair'
            if eco2 > 1000:
                rating = 'poor'
            if eco2 > 1500:
                rating = 'bad'
            return ECO2_Tuple(eco2, rating)
        else:
            return ECO2_Tuple(None, '')
        