from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_Unified import sleep_ms

ens160 = PiicoDev_ENS160()   # Initialise the ENS160 module
bme280 = PiicoDev_BME280()

while True:
    temperature, pressure, relative_humidity = bme280.values()
    ens160.temperature = temperature
    ens160.humidity = relative_humidity
    tvoc = ens160.tvoc
    eco2 = ens160.eco2
    
    # print total organic volatile compounds
#     print('TVOC: ' + str(tvoc) + ' ppb')
    
    # print equivalent CO2
    print('eCO2: ' + str(eco2.value) + ' ppm (' + str(eco2.rating) +')' + ' Temperature: ' + str(ens160.temperature) + ' Humidity: ' + str(ens160.humidity))
    sleep_ms(1000)