# main.py
import json
import network
from machine import RTC
from machine import Timer
import ntptime
import writeToLeds


rtc = RTC()

ntptime.settime()


def readSettings():
    """
    Reads settings from json.
    Returns tuple (wifi ssid, wifi password, timezone).
    """

    with open("config.json") as f:
        config = json.load(f)
    ssid = config["ssid"]
    password = config["password"]
    timezone = config["timezone"]
    return (ssid, password, timezone)


def setupClock():
    pass


def connectToWifi(ssid, password):
    """
    Function used to connect to WiFi.
    Takes SSID and password as parrameters.
    """

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print("connected to {}".format(config["ssid"]))


def convertTimezone(hour, timezone):
    """
    Takes time in format: hours, timezone(e.g. "+10" , "-5").
    and returns converted time.
    """
    if timezone == "0":
        return hour


def updateTime():
    time = rtc.datetime()
    writeToLeds.display_time(time[4] + 2, time[5])


tim = Timer(-1)
tim.init(
    period=500, mode=Timer.PERIODIC, callback=lambda t: updateTime()
)  # call updateTime() every 500 ms
