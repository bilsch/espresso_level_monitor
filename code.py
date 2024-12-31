import os
import time
import board
import gc
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import adafruit_ssd1327
import adafruit_vl6180x
import adafruit_ahtx0

try:
    cwd = ("/" + __file__).rsplit("/", 1)[0]
except:
    cwd = "/"

fonts = [
    file
    for file in os.listdir(cwd + "/fonts/")
    if (file.endswith(".bdf") and not file.startswith("._"))
]
for i, filename in enumerate(fonts):
    fonts[i] = cwd + "/fonts/" + filename

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

def draw_text(msg):
    display_height = 128
    display_width = 128
    display_font = fonts[0]
    font = bitmap_font.load_font(display_font)
    font.load_glyphs(msg.encode("utf-8"))
    splash = displayio.Group()
    display.root_group = splash

    # Make a background color fill
    color_bitmap = displayio.Bitmap(display_height, display_width, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    text = Label(font, text=msg)
    text.x = 20
    text.y = 100
    text.color = 0x0

    dims = text.bounding_box
    textbg_bitmap = displayio.Bitmap(dims[2], dims[3], 1)
    textbg_palette = displayio.Palette(1)
    textbg_palette[0] = 0xFF0000
    textbg_sprite = displayio.TileGrid(textbg_bitmap, pixel_shader=textbg_palette, x=text.x + dims[0], y=text.y + dims[1])
    splash.append(textbg_sprite)
    splash.append(text)
    display.refresh(target_frames_per_second=60)
    

while True:
    # just random stuff we may keep track of
    mem_free = gc.mem_free()

    # sensor readings
    range = distance_sensor.range
    temperature = aht20_sensor.temperature
    humidity = aht20_sensor.relative_humidity

    draw_text(f"temperature: {str(temperature)}\nhumidity: {str(humidity)}\nrange: {str(range)}")
    # msg=f"temperature: {str(temperature)}\nhumidity: {str(humidity)}\nrange: {str(range)}"
    
    time.sleep(5)