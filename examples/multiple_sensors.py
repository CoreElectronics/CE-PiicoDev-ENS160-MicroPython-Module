# Read from two sensors independently
from PiicoDev_ENS160 import PiicoDev_ENS160
from PiicoDev_Unified import sleep_ms

sensor_A = PiicoDev_ENS160(asw=0)  # Initialise the first sensor with ASW:OFF
sensor_B = PiicoDev_ENS160(asw=1)  # Initialise the second sensor with ASW:ON

while True:
    # Read the sensors
    tvoc_A = sensor_A.tvoc
    tvoc_B = sensor_B.tvoc
    
    # print total organic volatile compounds
    print('A: ' + str(tvoc_A) + '    B: ' + str(tvoc_B))
    
    sleep_ms(1000)
