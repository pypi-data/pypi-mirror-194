import argparse

from ecowatti import Ecowatti, EcowattiConfig
from typing import List


def main(device: str, timeout: int, sensors: List[str], all_sensors: bool):
    config = EcowattiConfig(device, serial_timeout=timeout)
    ecowatti = Ecowatti(config)

    ecowatti.update_all_temperatures()

    if all_sensors:
        for sensor in ecowatti._temperature_sensors:
            print(sensor.name, sensor.value)

    elif sensors:
        for sensor in sensors:
            if sensor == "T1":
                print(ecowatti.T1.name, ecowatti.T1.value)
            elif sensor == "T2":
                print(ecowatti.T2.name, ecowatti.T2.value)
            elif sensor == "T3":
                print(ecowatti.T3.name, ecowatti.T3.value)
            elif sensor == "T4":
                print(ecowatti.T4.name, ecowatti.T4.value)
            elif sensor == "T5":
                print(ecowatti.T5.name, ecowatti.T5.value)
            elif sensor == "T6":
                print(ecowatti.T6.name, ecowatti.T6.value)
            elif sensor == "T7":
                print(ecowatti.T7.name, ecowatti.T7.value)
            elif sensor == "T8":
                print(ecowatti.T8.name, ecowatti.T8.value)
            elif sensor == "T9":
                print(ecowatti.T9.name, ecowatti.T9.value)
            elif sensor == "T10":
                print(ecowatti.T10.name, ecowatti.T10.value)
            else:
                print(f"Uknown sensor: {sensor}")
    else:
        print("No sensors defined.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Ecowatti", description="Read values from Jäspi Ecowatti boiler")

    parser.add_argument(
        "-d", "--device", help="Specify Serial device. Example: -d /dev/ttyUSB0")
    parser.add_argument("-t", "--timeout",
                        help="Specify Serial timeout in seconds. Default = 1", default=1)

    sensors = parser.add_mutually_exclusive_group(required=True)
    sensors.add_argument(
        "-s", "--sensor", help="Specify sensors to read T1-T10. Example = -s T1", action='append')
    sensors.add_argument(
        "-a", "--all", help="Read all sensor values", action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    main(args.device, args.timeout, args.sensor, args.all)
