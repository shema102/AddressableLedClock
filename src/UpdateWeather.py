import math
import urequests

apiKey = "&appid=a988988f9b8811b3d5b23b888af9a7ca"
url = "api.openweathermap.org/data/2.5/weather?q="
city = "Kyiv"

url = "https://" + url + city + "&units=metric" + apiKey

response = urequests.get(url)

parsed = response.json()
if parsed["cod"] == 200:
    weather = {
        "temperature": math.ceil(parsed["main"]["temp"]),
        "pressure": math.ceil(parsed["main"]["pressure"] * 0.75006375541921),
        "humidity": parsed["main"]["humidity"],
        "clouds": parsed["clouds"]["all"],
        "wind_speed": parsed["wind"]["speed"],
        "wind_direction": parsed["wind"]["deg"],
    }
else:
    print("Error {}".format(parsed["cod"]))

response.close()
