import machine
import neopixel

led_pin = 14
led_num = (
    2 * 7 * 4 + 2
)  # 4 numbers of 7 segments 2 led per segment and 2 led separartor
np = neopixel.NeoPixel(machine.Pin(led_pin), led_num)

# sumbols, order of elements g e d c b a f (as in 7 segment display):
num = (
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # 0
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0),  # 2
    (1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),  # 3
    (1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1),  # 4
    (1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1),  # 5
    (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1),  # 6
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # 9
)
no_num = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  # blank
separator = (1, 1)

black = (0, 0, 0)
red = (255, 0, 0)


def timeToStr(hour, minute):
    h = str(hour)
    m = str(minute)
    if len(h) == 1:
        h = "n" + h
    if len(m) == 1:
        m = "0" + m
    return h + ":" + m


def display_time(hour, minute):
    cur_time = timeToStr(hour, minute)
    cur_time = cur_time.replace(":", "")
    cur_time = "".join(reversed(cur_time))
    buffer = []
    for t in cur_time:
        if t == "n":
            buffer.extend(no_num)
        else:
            buffer.extend(num[int(t)])
    buffer.extend(separator)  # add separator

    for index, item in enumerate(buffer):
        if buffer[index] == 0:
            buffer[index] = black
        else:
            buffer[index] = red

    for index, item in enumerate(buffer):
        np[index] = buffer[index]
    # print(buffer)
    np.write()
