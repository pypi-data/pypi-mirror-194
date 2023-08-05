# Ecowatti

Simple utility to read values from Jäspi Ecowatti boiler.

## Installation

Install using pip

```
pip install ecowatti
```

## Usage

Basic usage is to import Ecowatti and EcowattiConfig.

Initialize EcowattiConfig with proper settings and use it to initialize Ecowatti itself.

```
from ecowatti import Ecowatti, EcowattiConfig

config = EcowattiConfig("/dev/ttyUSB0", serial_timeout=1)
ecowatti = Ecowatti(config)

ecowatti.update_all_temperatures()

for sensor in ecowatti._temperature_sensors:
    print(sensor.description, sensor.value)
```

## Command-line usage

Basic command-line usage

### Display all sensors and their values

```
|> python3 -m ecowatti -d /dev/ttyUSB0 -a
T1 22.1
T2 0.4
T3 None
T4 23.3
T5 22.1
T6 22.7
T7 None
T8 21.6
T9 51.0
T10 3.5
```

### Display values for specific sensors

```
|> python3 -m ecowatti -d /dev/ttyUSB0 -s T1 -s T5 -s T6
T1 22.1
T5 22.1
T6 22.7

```
