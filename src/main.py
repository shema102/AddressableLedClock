# main.py
import json
import network
from machine import RTC
from machine import Timer
import ntptime
import ledController


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
    print(f"connected to {ssid}")


def convertTimezone(hour, timezone):
    """
    Takes time in format: hours, timezone(e.g. "0", "+10" , "-5").
    and returns converted time.
    """
    if timezone[0] == "-":
        timezone = int(timezone.replace("-", ""))
        hour = hour - timezone
    elif timezone[0] == "+":
        timezone = int(timezone.replace("+", ""))
        hour = hour + timezone

    if hour >= 24:
        hour -= 24
    elif hour < 0:
        hour += 24
    return hour


def updateTime(timezone):
    time = rtc.datetime()
    hour = convertTimezone(time[4], timezone)
    minute = time[5]
    ledController.display_time(hour, minute)


rtc = RTC()  # rtc hanlde
ntptime.settime()  # updating time from net

tim = Timer(-1)
tim.init(
    period=500, mode=Timer.PERIODIC, callback=lambda t: updateTime()
)  # call updateTime() every 500 ms
