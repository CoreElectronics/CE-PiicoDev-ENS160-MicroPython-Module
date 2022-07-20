# PiicoDev® Air Quality Sensor ENS160 MicroPython Module

This is the firmware repo for the [Core Electronics PiicoDev® Air Quality Sensor ENS160](https://core-electronics.com.au/catalog/product/view/sku/CE08560)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guide](https://piico.dev/p23)

<!-- TODO verify the tested-devices list 
This module has been tested on:
 - Micro:bit v2
 - Raspberry Pi Pico
 - Raspberry Pi SBC
-->

# Initialisation

## `PiicoDev_Potentiometer(bus=, freq=, sda=, scl=, address=0x53, address_switch=, asw=, intdat=False, intgpr=False, int_cfg=0, intpol=0, temperature=20, humidity=50)`
| Parameter             | Type  | Range            | Default                               | Description |
| --------------------- | ----- | ---------------- | ------------------------------------- | --- |
| bus                   | int   | 0,1              | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit |
| freq                  | int   | 100 to 1000000   | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi |
| sda                   | Pin   | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only |
| scl                   | Pin   | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only |
| address               | int   | 0x53             | 0x52, 0x53                            | Manually specify the address of the connected device |
| address_switch or asw | int   | 0=OFF 1=ON       | None                                  | Hardware switches change the device address - Abstracts the need for user to look up an address, simply input the switch position. Alternatively, use `address` for explicit address. |
| intdat                | bool  |                  | False                                 | INTn pin asserted when new data is presented in the DATA_XXX Registers |
| intgpr                | bool  |                  | False                                 | 100.0 | INTn pin asserted when new data is presented in the General Purpose Read Registers |
| int_cfg               | int   | 0, 1             | False                                 | INTn pin drive: 0: Open drain 1: Push / Pull |
| intpol                | int   | 0, 1             | False                                 | INTn pin polarity: 0: Active low (Default) 1: Active high |
| temperature           | float |                  | 20.0                                  | The current temperature |
| humidity              | float |                  | 50.0                                  | The current humidity |

## Properties

### `.value`
Returns a float between 0.0 and 100.0 (default) or a value from a user-defined scale

**Example Usage**
```python
value = pot.value
```

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
