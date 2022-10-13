# Read air quality metrics from the PiicoDev Air Quality Sensor ENS160
# Shows three metrics: AQI, TVOC and eCO2

from PiicoDev_ENS160 import PiicoDev_ENS160 # import the device driver
from PiicoDev_Unified import sleep_ms       # a cross-platform sleep function

sensor = PiicoDev_ENS160()   # Initialise the ENS160 module

while True:
    # Read from the sensor
    aqi = sensor.aqi
    tvoc = sensor.tvoc
    eco2 = sensor.eco2
    
    # Print air quality metrics
    print('    AQI: ' + str(aqi.value) + ' [' + str(aqi.rating) +']')
    print('   TVOC: ' + str(tvoc) + ' ppb')
    print('   eCO2: ' + str(eco2.value) + ' ppm [' + str(eco2.rating) +']')
    print(' Status: ' + sensor.operation)
    print('--------------------------------')
    
    sleep_ms(1000)