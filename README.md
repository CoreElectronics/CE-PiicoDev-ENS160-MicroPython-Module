# PiicoDev® Air Quality Sensor ENS160 MicroPython Module

This is the firmware repo for the [Core Electronics PiicoDev® Air Quality Sensor ENS160](https://core-electronics.com.au/catalog/product/view/sku/CE08560)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guide](https://piico.dev/p23)

# Initialisation

## `PiicoDev_ENS160(bus=, freq=, sda=, scl=, address=0x53, asw=, intdat=False, intgpr=False, int_cfg=0, intpol=0, temperature=25, humidity=50)`
| Parameter   | Type  | Range            | Default                               | Description |
| ----------- | ----- | ---------------- | ------------------------------------- | --- |
| bus         | int   | 0,1              | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit |
| freq        | int   | 100 to 1000000   | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi |
| sda         | Pin   | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only |
| scl         | Pin   | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only |
| address     | int   | 0x53             | 0x52, 0x53                            | Manually specify the address of the connected device |
| asw         | int   | 0=OFF 1=ON       | None                                  | Hardware switch changes the device address. Abstracts the need for user to look up an address, simply input the switch position. Alternatively, use `address` for explicit address. |
| intdat      | bool  |                  | False                                 | INT pin asserted when new data is presented in the DATA_XXX Registers |
| intgpr      | bool  |                  | False                                 | INT pin asserted when new data is presented in the General Purpose Read Registers 
| int_cfg     | int   | 0, 1             | False                                 | INTn pin drive: 0: Open drain 1: Push / Pull |
| intpol      | int   | 0, 1             | False                                 | INTn pin polarity: 0: Active low (Default) 1: Active high |
| temperature | float |                  | 25.0                                  | The current temperature |
| humidity    | float |                  | 50.0                                  | The current humidity |

## Properties

### `.temperature`
Sets the temperature

**Example Usage**
```python
sensor.temperature = 24.3
print(sensor.temperature)
```

### `.humidity`
Sets the humidity

**Example Usage**
```python
sensor.humidity = 55.3
print(sensor.humidity)
```

### `.aqi`
Reads the Air Quality Index according to UBA [1..5].  The AQI-UBA air quality index is derived from a guideline by the German Federal Environmental Agency based on a Total Volatile Organic Compounds (TVOC) sum signal. Although a local, German guideline, it is referenced and adopted by many countries and organizations.

**Example Usage**
```python
aqi = sensor.aqi
print(aqi.value)
print(aqi.rating)
```

### `.tvoc`
Reads the calculated Total Volatile Organic Compounds (TVOC) concentration in ppb.

**Example Usage**
```python
tvoc = sensor.tvoc
print(tvoc.value)
print(tvoc.rating)
```

### `.eco2`
Reads the calculated equivalent CO2-concentration in ppm, based on the detected VOCs and hydrogen

**Example Usage**
```python
eco2 = sensor.eco2
print(eco2)
```

### `.status_validity_flag`
Reads the validity flag.  Returns 0 = 'operating ok', 1 = 'warm-up', 2 = 'initial start-up', 3 = 'no valid output'.

**Example Usage**
```python
print(sensor.status_validity_flag)
```

### `.operation`
Reads the validity flag.  Returns 'operating ok', 'warm-up', 'initial start-up', 'no valid output'.

**Example Usage**
```python
print(sensor.operation)
```

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
