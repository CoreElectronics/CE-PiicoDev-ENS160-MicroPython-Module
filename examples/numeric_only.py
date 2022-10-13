from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_Unified import sleep_ms
 
sensor = PiicoDev_ENS160()   # Initialise the ENS160 module

while True:
    # Read the sensor
    tvoc = sensor.tvoc
    eco2 = sensor.eco2
    
    # print total organic volatile compounds
    print('TVOC: ' + str(tvoc) + ' ppb')
    
    # print equivalent CO2
#     print('eCO2: ' + str(eco2.value) + ' ppm ')
    
    sleep_ms(1000)
