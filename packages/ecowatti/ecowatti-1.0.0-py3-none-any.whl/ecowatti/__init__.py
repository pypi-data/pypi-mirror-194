from __future__ import annotations

from crc import Calculator, Configuration
from serial import Serial
from datetime import datetime, timedelta
from typing import List

import argparse


class MeasurePoint:
    value: float | None
    memory_location: int
    name: str
    description: str

    def __init__(self, memory_location: int, name: str, description: str) -> None:
        self.value = None
        self.memory_location = memory_location
        self.name = name
        self.description = description


class EcowattiConfig:
    serial_port: str
    serial_timeout: float
    response_timeout: int

    def __init__(self, serial_port: str, response_timeout: int = 2, serial_timeout: float = 0.00001):
        self.serial_port = serial_port
        self.response_timeout = response_timeout
        self.serial_timeout = serial_timeout


class Ecowatti:
    T1: MeasurePoint
    T2: MeasurePoint
    T3: MeasurePoint
    T4: MeasurePoint
    T5: MeasurePoint
    T6: MeasurePoint
    T7: MeasurePoint
    T8: MeasurePoint
    T9: MeasurePoint
    T10: MeasurePoint

    _config: EcowattiConfig
    _serial: Serial
    _request_id: int
    _crc_calculator: Calculator
    _crc_config: Configuration
    _temperature_sensors: List[MeasurePoint]

    def __init__(self, config: EcowattiConfig):
        self._crc_config = Configuration(
            width=8,
            polynomial=0x81,
            init_value=0x4e,
            reverse_input=True,
            reverse_output=True,
            final_xor_value=0x00
        )

        self._crc_calculator = Calculator(self._crc_config)
        self._config = config
        self._request_id = 0x40

        self._serial = Serial(self._config.serial_port,
                              115200, timeout=self._config.serial_timeout)

        self.T1 = MeasurePoint(0x00, "T1", "Lämmityspiirin menovesi")
        self.T2 = MeasurePoint(0x01, "T2", "Ulkolämpötila")
        self.T3 = MeasurePoint(0x02, "T3", "Muu lämmönlähde")
        self.T4 = MeasurePoint(0x03, "T4", "Lataussäiliön alaosa")
        self.T5 = MeasurePoint(0x04, "T5", "Lataussäiliön yläosa")
        self.T6 = MeasurePoint(0x05, "T6", "Lämmityspiirien paluuvesi")
        self.T7 = MeasurePoint(0x06, "T7", "Lämmityspiirin 2 menovesi")
        self.T8 = MeasurePoint(
            0x07, "T8", "Aurinkojärjestelmän varaajan anturi")
        self.T9 = MeasurePoint(0x08, "T9", "Käyttövesi")
        self.T10 = MeasurePoint(0x09, "T10", "Aurinkokeräimet")

        self._temperature_sensors = [
            self.T1, self.T2, self.T3, self.T4, self.T5, self.T6, self.T7, self.T8, self.T9, self.T10]

    def _generate_message(self, mem_location: int) -> bytearray:
        # ['a3', 'fd', '07', 'a2', '81', '81', '40', 'aa', '07', 'f8']
        header = 0xa3                               # 0
        sender = 0xfd                               # 1
        length = 0x07                               # 2
        constant_1 = 0xa2                           # 3
        constant_2 = 0x81                           # 4
        constant_3 = 0x81                           # 5
        request_id = self._request_id               # 6
        constant_4 = 0xaa                           # 7
        memory_location = mem_location              # 8

        message = bytearray([header, sender, length, constant_1, constant_2,
                            constant_3, request_id, constant_4, memory_location])
        message.append(self._crc_calculator.checksum(message))   # 9

        return message

    def _read_message(self) -> bytearray:
        buffer = bytearray()
        data_len = 100

        while True:
            if data_len > 0:
                data_len -= 1

            # Handle random msgs
            elif len(buffer) == 2:
                if buffer[1] not in [0xfd, 0x20, 0x24]:
                    return buffer

            else:
                if buffer:
                    return buffer

            byte = self._serial.read()

            if byte == b"\xa3":
                # Find the pakcet header and start gathering the array
                buffer.append(int.from_bytes(byte, "little"))
            elif len(buffer) != 0 and byte != b"":
                # Check that the array is not empty, so we don't create half a packet. Also check that the result from EcoWatti is not empty string.
                buffer.append(int.from_bytes(byte, "little"))

            if len(buffer) == 3:
                # Store the package length
                data_len = int.from_bytes(byte, "little")

    def update_value(self, measure_point: MeasurePoint) -> None:

        if not self._serial.is_open:
            self._serial.open()

        message = self._generate_message(measure_point.memory_location)

        retry_time = datetime.now()+timedelta(seconds=self._config.response_timeout)

        self._serial.write(message)
        retry_count = 63

        while True:
            response = self._read_message()

            try:
                if response[6] == self._request_id:
                    # Check if our response and save the value
                    int_value = int.from_bytes(
                        response[9:11], "little", signed="True")

                    # 32767 == Sensor not connected
                    if int_value == 32767:
                        measure_point.value = None
                    else:
                        measure_point.value = int_value/10

                    self._request_id += 1
                    break
            except IndexError:
                pass

            if datetime.now() > retry_time:
                # No response with this request id within 2 seconds. Moving to next id.
                retry_time = datetime.now()+timedelta(seconds=self._config.response_timeout)
                retry_count -= 1

                if retry_count == 0:
                    break

                # Update the request id. If above 0x7f we start again from 0x40
                if self._request_id+1 > 0x7f:
                    self._request_id = 0x40
                else:
                    self._request_id = self._request_id+1

                message = self._generate_message(measure_point.memory_location)

                self._serial.write(message)

    def update_all_temperatures(self) -> None:
        for temp_sensor in self._temperature_sensors:
            self.update_value(temp_sensor)
