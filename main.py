from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_Unified import sleep_ms
 
sensor = PiicoDev_ENS160()   # Initialise the ENS160 module

print('       statas: ' + str(sensor.statas))
print('       stater: ' + str(sensor.stater))
print('validity_flag: ' + str(sensor.validity_flag))
print('       newdat: ' + str(sensor.newdat))
print('       newgpr: ' + str(sensor.newgpr))
while True:
    sensor.getDeviceStatus()
#     print('Temperature: ' + str(sensor.getTemperature()))
#     print('Humidity: ' + str(sensor.getHumidity()))
    print('       statas: ' + str(sensor.statas))
    print('       stater: ' + str(sensor.stater))
    print('validity_flag: ' + str(sensor.validity_flag))
    print('       newdat: ' + str(sensor.newdat))
    print('       newgpr: ' + str(sensor.newgpr))
#    print('AQI: ' + str(sensor.readAQI()))
#    print('TVOC: ' + str(sensor.readTVOC()))
#    print('ECO2: ' + str(sensor.readECO2()))
    print(str(sensor.aqi) + ',' + str(sensor.tvoc) + ',' + str(sensor.eco2))
    sleep_ms(1000)
    
