from os import getenv
from time import sleep
import board

import wifi
import socketpool
import displayio
import terminalio
from adafruit_connection_manager import get_radio_socketpool
from adafruit_httpserver import Server, Request, Response, REQUEST_HANDLED_RESPONSE_SENT

from adafruit_display_text import label
import adafruit_ssd1327
import adafruit_vl6180x

# Set up wifi
ssid = getenv("CIRCUITPY_WIFI_SSID")
wifi_pass = getenv("CIRCUITPY_WIFI_PASSWORD")
hostname = getenv("HOSTNAME")

if ssid is None or wifi_pass is None or hostname is None:
    print("Error you must set CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD in settings.toml")
    exit(1)

try:
    wifi.radio.hostname = hostname
    wifi.radio.connect(ssid=ssid, password=wifi_pass)
    pool = socketpool.SocketPool(wifi.radio)
    print("My IP address is", wifi.radio.ipv4_address)
except:
    print(f"Failed to connect to {ssid}")
    exit(1)

pool = get_radio_socketpool(wifi.radio)
server = Server(pool, "/static")

# i2c boards:
#   0x3c: 128x128 oled
#   0x29: VL6180 time of flight sensor
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_ssd1327.SSD1327(display_bus, width=128, height=128)

# distance sensor details
distance_sensor = adafruit_vl6180x.VL6180X(i2c)
# These are TODO
# Need to mount the sensor and take a reading at empty and full levels
empty_level = 255
full_level = 20

def draw_text(text, scale=1):
    splash = displayio.Group()
    display.root_group = splash

    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_width = text_area.bounding_box[2] * scale
    text_group = displayio.Group(
        scale=scale,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

def get_range(distance_sensor):
    range = distance_sensor.range
    return range

@server.route("/")
def range_http(request: Request):
    range = get_range(distance_sensor)
    return Response(request, f"range: {range}")

# Note the server is essentially a background task
server.start("0.0.0.0", 8080)

while True:
    range = get_range(distance_sensor)
    msg = f"range: {str(range)}"
    draw_text(msg)
    sleep(0.5)
    
    try:
        # Do something useful in this section,
        # for example read a sensor and capture an average,
        # or a running total of the last 10 samples

        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass
    except OSError as error:
        print(error)
        continue