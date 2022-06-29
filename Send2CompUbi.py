import sys
import bme280
import requests
import os
import time
import board
import time
import adafruit_mcp3xxx.mcp3008 as MPC
from adafruit_mcp3xxx.analog_in import AnalogIn
from gpiozero import CPUTemperature
from datetime import datetime

cpu = CPUTemperature().temperature
airtemp, pressure, humidity = bme280.readBME280All()


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0)

coMv = chan.voltage
coValue = (coMv * 200 / 4.82)

os.system("pon rnet")
time.sleep(10)
try:

    url = "http://13.58.175.85:8081/dados"

    my_dict = {
        "co": str(coValue).strip(),
        "temperatura": str(airtemp).strip(),
        "umidade": str(humidity).strip(),
        "pressao": str(pressure).strip(),
        "data": str(coMv).strip(),
        "temperatura_cpu": str(cpu).strip(),
    }

    x = requests.post(url, json=my_dict)

except:
    print "error"

os.system("poff rnet")
