# main.py
import json
import network
from machine import RTC
from machine import Timer
import ntptime
import time
import ws

with open("config.json") as f:
    config = json.load(f)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config["ssid"], config["password"])
while not wlan.isconnected():
    pass
print("connected to {}".format(config["ssid"]))

rtc = RTC()

ntptime.settime()


def updateTime():
    time = rtc.datetime()
    ws.display_time(time[4] + 2, time[5])


tim = Timer(-1)
tim.init(period=500, mode=Timer.PERIODIC, callback=lambda t: updateTime())

# shows avaliable ram
# import gc
# gc.collect()
# gc.mem_free()
