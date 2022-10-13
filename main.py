from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_Unified import sleep_ms
 
sensor = PiicoDev_ENS160(temperature=26, humidity=71)   # Initialise the ENS160 module

print('       statas: ' + str(sensor.status_statas))
print('       stater: ' + str(sensor.status_stater))
print('validity_flag: ' + str(sensor.status_validity_flag))
print('       newdat: ' + str(sensor.status_newdat))
print('       newgpr: ' + str(sensor.status_newgpr))
print('Temperature: ' + str(sensor.temperature))
print('Humidity: ' + str(sensor.humidity))
while True:
    print('       statas: ' + str(sensor.status_statas))
    print('       stater: ' + str(sensor.status_stater))
    print('validity_flag: ' + str(sensor.status_validity_flag))
    print('validity_flag_desc: ' + str(sensor.operation))
    print('       newdat: ' + str(sensor.status_newdat))
    print('       newgpr: ' + str(sensor.status_newgpr))
#    print('AQI: ' + str(sensor.readAQI()))
#    print('TVOC: ' + str(sensor.readTVOC()))
#    print('ECO2: ' + str(sensor.readECO2()))
    aqi, aqi_rating = sensor.aqi
    print('rating ' + str(aqi_rating))
    eco2, eco2_rating = sensor.eco2
    print(str(aqi) + ': ' + aqi_rating + ',' + str(sensor.tvoc) + ',' + str(eco2) + ': ' + str(eco2_rating))
    sleep_ms(1000)
    
