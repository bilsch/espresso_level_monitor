import os
import time
import board
import gc
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_ssd1327
import adafruit_vl6180x
import adafruit_ahtx0


# i2c boards:
#   0x3c: 128x128 oled
#   0x29: VL6180 time of flight sensor
#   0x38: AHT20 temperature and humidity sensor
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_ssd1327.SSD1327(display_bus, width=128, height=128)

# distance sensor details
distance_sensor = adafruit_vl6180x.VL6180X(i2c)
# These are TODO
# Need to mount the sensor and take a reading at empty and full levels
empty_level = 255
full_level = 20

aht20_sensor = adafruit_ahtx0.AHTx0(i2c)

def draw_text(text, scale=1):
    splash = displayio.Group()
    display.root_group = splash

    # Draw a label
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
    text_width = text_area.bounding_box[2] * scale
    text_group = displayio.Group(
        scale=scale,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

while True:
    # sensor readings
    range = distance_sensor.range
    temperature = aht20_sensor.temperature
    humidity = aht20_sensor.relative_humidity

    draw_text(f"temperature: {str(temperature)}\nhumidity: {str(humidity)}\nrange: {str(range)}")
    # msg=f"temperature: {str(temperature)}\nhumidity: {str(humidity)}\nrange: {str(range)}"
    
    time.sleep(5)