_F='excellent'
_E='invalid'
_D='little'
_C='rating'
_B=False
_A=None
from PiicoDev_Unified import *
try:from ucollections import namedtuple;from ustruct import unpack
except:from collections import namedtuple;from struct import unpack
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=83
_REG_PART_ID=0
_REG_OPMODE=16
_REG_CONFIG=17
_REG_COMMAND=18
_REG_TEMP_IN=19
_REG_RH_IN=21
_REG_DEVICE_STATUS=32
_REG_DATA_AQI=33
_REG_DATA_TVOC=34
_REG_DATA_ECO2=36
_REG_DATA_T=48
_REG_DATA_RH=50
_REG_DATA_MISR=56
_REG_GPR_WRITE=64
_REG_GPR_READ=72
_BIT_CONFIG_INTEN=0
_BIT_CONFIG_INTDAT=1
_BIT_CONFIG_INTGPR=3
_BIT_CONFIG_INT_CFG=5
_BIT_CONFIG_INTPOL=6
_BIT_DEVICE_STATUS_NEWGPR=0
_BIT_DEVICE_STATUS_NEWDAT=1
_BIT_DEVICE_STATUS_VALIDITY_FLAG=2
_BIT_DEVICE_STATUS_STATER=6
_BIT_DEVICE_STATUS_STATAS=7
_VAL_PART_ID=352
_VAL_OPMODE_DEEP_SLEEP=0
_VAL_OPMODE_IDLE=1
_VAL_OPMODE_STANDARD=2
_VAL_OPMODE_RESET=240
AQI_Tuple=namedtuple('AQI',('value',_C))
ECO2_Tuple=namedtuple('eCO2',('value',_C))
def _read_bit(x,n):return x&1<<n!=0
def _read_crumb(x,n):return _read_bit(x,n)+_read_bit(x,n+1)*2
def _read_tribit(x,n):return _read_bit(x,n)+_read_bit(x,n+1)*2+_read_bit(x,n+2)*4
def _set_bit(x,n):return x|1<<n
def _clear_bit(x,n):return x&~(1<<n)
def _write_bit(x,n,b):
	if b==0:return _clear_bit(x,n)
	else:return _set_bit(x,n)
class PiicoDev_ENS160:
	def __init__(self,bus=_A,freq=_A,sda=_A,scl=_A,address=_I2C_ADDRESS,asw=_A,intdat=_B,intgpr=_B,int_cfg=0,intpol=0,temperature=25.0,humidity=50.0):
		if asw==0:self.address=_I2C_ADDRESS
		elif asw==1:self.address=_I2C_ADDRESS-1
		else:self.address=address
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);config=0
		if intdat or intgpr:config=_set_bit(config,_BIT_CONFIG_INTEN);config=_write_bit(config,_BIT_CONFIG_INTDAT,intdat);config=_write_bit(config,_BIT_CONFIG_INTGPR,intgpr)
		config=_write_bit(config,_BIT_CONFIG_INT_CFG,int_cfg);config=_write_bit(config,_BIT_CONFIG_INTPOL,intpol);self.config=config;self._aqi=_A;self._tvoc=_A;self._eco2=_A
		try:
			part_id=self._read_int(_REG_PART_ID,2)
			if part_id!=_VAL_PART_ID:print('Device is not PiicoDev ENS160');raise SystemExit
			self._write_int(_REG_OPMODE,_VAL_OPMODE_STANDARD,1);sleep_ms(20);opmode=self._read_int(_REG_OPMODE,1);sleep_ms(20);self._write_int(_REG_CONFIG,self.config,1);self.temperature=temperature;self.humidity=humidity
		except Exception as e:print(i2c_err_str.format(self.address));raise e
	def _read(self,register,length=1,bytestring=_B):
		try:
			d=self.i2c.readfrom_mem(self.address,register,length)
			if bytestring:return bytes(d)
			return d
		except:print(i2c_err_str.format(self.address));return _A
	def _write(self,register,data):
		try:return self.i2c.writeto_mem(self.address,register,data)
		except:print(i2c_err_str.format(self.address));return _A
	def _read_int(self,register,length=1):return int.from_bytes(self._read(register,length),_D)
	def _write_int(self,register,integer,length=1):return self._write(register,int.to_bytes(integer,length,_D))
	def _read_data(self):
		device_status=self._read_int(_REG_DEVICE_STATUS)
		if _read_bit(device_status,_BIT_DEVICE_STATUS_NEWDAT)is True:data=self._read(_REG_DEVICE_STATUS,6,bytestring=True);self._status,self._aqi,self._tvoc,self._eco2=unpack('<bbhh',data)
	@property
	def humidity(self):return self._read_int(_REG_DATA_RH,2)/512
	@humidity.setter
	def humidity(self,humidity):self._write_int(_REG_RH_IN,int(humidity)*512,2)
	@property
	def temperature(self):kelvin=self._read_int(_REG_DATA_T,2)/64;return kelvin-273.15
	@temperature.setter
	def temperature(self,temperature):kelvin=temperature+273.15;self._write_int(_REG_TEMP_IN,int(kelvin*64),2)
	@property
	def status(self):self._read_data();return self._status
	@property
	def status_statas(self):return _read_bit(self.status,_BIT_DEVICE_STATUS_STATAS)
	@property
	def status_stater(self):return _read_bit(self.status,_BIT_DEVICE_STATUS_STATER)
	@property
	def status_newdat(self):return _read_bit(self.status,_BIT_DEVICE_STATUS_NEWDAT)
	@property
	def status_newgpr(self):return _read_bit(self.status,_BIT_DEVICE_STATUS_NEWGPR)
	@property
	def status_validity_flag(self):return _read_crumb(self.status,_BIT_DEVICE_STATUS_VALIDITY_FLAG)
	@property
	def operation(self):return['operating ok','warm-up','initial start-up','no valid output'][self.status_validity_flag]
	@property
	def aqi(self):
		self._read_data()
		if self._aqi is not _A:ratings={0:_E,1:_F,2:'good',3:'moderate',4:'poor',5:'unhealthy'};aqi=_read_tribit(self._aqi,0);return AQI_Tuple(aqi,ratings[aqi])
		else:return AQI_Tuple(_A,'')
	@property
	def tvoc(self):
		self._read_data()
		if self._tvoc is not _A:return self._tvoc
		else:return _A
	@property
	def eco2(self):
		self._read_data()
		if self._eco2 is not _A:
			eco2=self._eco2;rating=_E
			if eco2>=400:rating=_F
			if eco2>600:rating='good'
			if eco2>800:rating='fair'
			if eco2>1000:rating='poor'
			if eco2>1500:rating='bad'
			return ECO2_Tuple(eco2,rating)
		else:return ECO2_Tuple(_A,'')