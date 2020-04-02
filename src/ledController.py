import machine
import neopixel

led_pin = 14
led_num = 2 * 7 * 4 + 2
# 4 numbers of 7 segments 2 led per segment and 2 led ":" separartor
np = neopixel.NeoPixel(machine.Pin(led_pin), led_num)

# sumbols, order of elements g e d c b a f (as in 7 segment display):
symbol = {
    "0": (0, 1, 1, 1, 1, 1, 1),
    "1": (0, 0, 0, 1, 1, 0, 0),
    "2": (1, 1, 1, 0, 1, 1, 0),
    "3": (1, 0, 1, 1, 1, 1, 0),
    "4": (1, 0, 0, 1, 1, 0, 1),
    "5": (1, 0, 1, 1, 0, 1, 1),
    "6": (1, 1, 1, 1, 0, 1, 1),
    "7": (0, 0, 0, 1, 1, 1, 0),
    "8": (1, 1, 1, 1, 1, 1, 1),
    "9": (1, 0, 1, 1, 1, 1, 1),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ":": (1, 1),
}

colors = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "yellow": "#ffff00",
}


def hexToRgb(hexValue):
    """
    Takes hex value of coror and returns rgb tuple.
    """
    h = hexValue.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def setBrightness(rgbTuple, brightness):
    """
    Function takes tuple of RGB values and changes value based on level if brightness (1 - 10).
    """
    return tuple([(value // 10) * brightness for value in rgbTuple])


def setColor(listToColorise, color, brightness=10, mode="solid"):
    """
    Takes list of zeros and ones and replaces every of ones with RGB tuple,
    every zero with (0,0,0).
    Returns list of tuples.
    Mode changes how colors spread in list:
    Solid - one solid color;
    Rainbow - colors chouse randomly from colors dict.

    For solid colors brightness can be changed.
    """
    if mode == "solid":
        # go through all leds except last two (":" separator)
        color = hexToRgb(colors[color])
        black = hexToRgb(colors["black"])
        for i in range(0, led_num - 2, 2):
            if listToColorise[i] == 1:
                listToColorise[i] = setBrightness(color, brightness)
                listToColorise[i + 1] = setBrightness(color, brightness)
            else:
                listToColorise[i] = black
                listToColorise[i + 1] = black
        # set color to separator
        if listToColorise[-2] == 1:
            listToColorise[-2] = setBrightness(color, brightness)
            listToColorise[-1] = setBrightness(color, brightness)
        else:
            listToColorise[-2] = black
            listToColorise[-1] = black
        return listToColorise


def displayTime(hour, minute, color, brightness=5):
    hour = str(hour)
    if len(hour) == 1:
        # if in houres we have only one digit add whitespace, so we don't get solething like "09:15" on clock
        hour = " " + hour
    minute = str(minute)
    if len(minute) == 1:
        minute = "0" + minute
    time = "".join(reversed(hour + minute))
    # reversed becauce we start filling numbers from least significant digit
    buffer = []
    for number in time:
        for bit in symbol[number]:
            buffer.append(bit)
            buffer.append(bit)
    buffer.extend(symbol[":"])  # add separator
    bufferCollored = setColor(buffer, color, brightness)
    for index, value in enumerate(bufferCollored):
        np[index] = value
    np.write()
