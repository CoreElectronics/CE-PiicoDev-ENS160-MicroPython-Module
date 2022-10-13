# Read air quality metrics from the PiicoDev Air Quality Sensor ENS160
# Shows three metrics: AQI, TVOC and eCO2

from PiicoDev_ENS160 import PiicoDev_ENS160 # import the device driver
from PiicoDev_Unified import sleep_ms       # a cross-platform sleep function
from machine import Pin

sensor = PiicoDev_ENS160()   # Initialise the ENS160 module
led = Pin(25, Pin.OUT)

log = open('/log.csv','a')
sample = 0
while True:
    led.toggle()
    try:
            
        # Read from the sensor
        aqi = sensor.aqi
        tvoc = sensor.tvoc
        eco2 = sensor.eco2
        
        log.write('{},{},{},{}\n'.format(sample, aqi.value, eco2.value, tvoc))
        
        
    except KeyboardInterrupt:
        log.close()
    except:
        pass
    
    sample += 1
    sleep_ms(1000)
