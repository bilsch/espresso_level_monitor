# espresso_level_monitor
My hacky espresso water resevoir level monitor

## Boards

There are a few different boards used in this setup:

1. [Raspberry Pi Pico 2W](https://www.adafruit.com/product/6087)
    * probably overkill but its so darn cheap!
1. [PiCowbell](https://www.adafruit.com/product/5200) for the pico
    * Technically overkill you could just wire in i2c direct to the board

Then a few different i2c boards:

1. [128x128 oled](https://www.sparkfun.com/products/15890) from Sparkfun (had this laying around)
1. [VL6180](https://www.adafruit.com/product/3316) time of flight sensor
1. [AHT20](https://www.adafruit.com/product/4566) temperature and humidity sensor

## The code

This is still in progress. Fiddling with the lcd, just not doing what I want it to do but I think its close.