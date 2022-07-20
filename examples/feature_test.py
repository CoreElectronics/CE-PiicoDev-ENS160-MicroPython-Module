from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_Unified import sleep_ms

sensor = PiicoDev_ENS160()   # Initialise the ENS160 module

while True:
    sensor.temperature = 46.3
    sensor.humidity = 52.4
    aqi = sensor.aqi
    tvoc = sensor.tvoc
    eco2 = sensor.eco2
    
    print('        AQI: ' + str(aqi.value) + ' ppm [' + str(aqi.rating) +']')
    print('       TVOC: ' + str(tvoc) + ' ppm')
    print('       eCO2: ' + str(eco2.value) + ' ppm [' + str(eco2.rating) +']')
    print('Temperature: ' + str(sensor.temperature))
    print('   Humidity: ' + str(sensor.humidity))
    print('   Validity: ' + str(sensor.status_validity_flag) + ' [' + str(sensor.status_validity_flag_description) + ']')
    print('--------------------------------')
    sleep_ms(1000)