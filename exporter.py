import socket
import time

import board
import busio
import adafruit_bme280

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

SENSOR_ADDR = 0x76
# Based on my local weather report, it makes it vaguely accurate
AIR_PRESSURE = 30.08 * (1013.25 / 29.92)
 
class BMP280Exporter(object):
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=SENSOR_ADDR)
        self.sensor.sea_level_pressure = AIR_PRESSURE
        self.hostname = socket.gethostname()

    def collect(self):
        temp_guage = GaugeMetricFamily('temperature', 'Current temperature in celsius', labels=['host','sensor_type'])
        temp_guage.add_metric([self.hostname,'BME280'], round(self.sensor.temperature, 2))
        yield temp_guage
        humidity_guage = GaugeMetricFamily('humidity', 'Current realtive humidity', labels=['host','sensor_type'])
        humidity_guage.add_metric([self.hostname,'BME280'], round(self.sensor.humidity, 2))
        yield humidity_guage
        pressure_guage = GaugeMetricFamily('pressure', 'Current atmospheric pressure in hPa', labels=['host','sensor_type'])
        pressure_guage.add_metric([self.hostname,'BME280'], round(self.sensor.pressure, 2))
        yield pressure_guage


if __name__ == "__main__":
    REGISTRY.register(BMP280Exporter())
    start_http_server(8000)
    running = True
    while running:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            running = False