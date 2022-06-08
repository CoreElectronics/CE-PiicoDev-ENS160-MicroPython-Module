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

_BIT_CONFIG_INTPOL  = 6
_BIT_CONFIG_INT_CFG = 5
_BIT_CONFIG_INTGPR  = 3
_BIT_CONFIG_INTDAT  = 1
_BIT_CONFIG_INTEN   = 0

_VAL_PART_ID           = 0x160
_VAL_OPMODE_DEEP_SLEEP = 0x00
_VAL_OPMODE_IDLE       = 0x01
_VAL_OPMODE_STANDARD   = 0x02
_VAL_OPMODE_RESET      = 0xF0


class PiicoDev_ENS160(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, address=_I2C_ADDRESS):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.address = address
        try:
            part_id = int.from_bytes(self.i2c.readfrom_mem(self.address, _REG_PART_ID, 2),'little')
            if part_id != _VAL_PART_ID:
                print('Device is not PiicoDev ENS160')
                raise SystemExit
            self.i2c.writreto_mem(self.address, __REG_OPMODE, _VAL_OPMODE_STANDARD)
            
        except Exception as e:
            print(i2c_err_str.format(self.address))
            raise e
