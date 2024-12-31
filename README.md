# espresso_level_monitor
My hacky espresso water resevoir level monitor

So the basic idea here is to get a sensor reading to indicate water level in the resevoir of my espresso machine. Right now the only way I find out I'm low on water is when the sensor in the machine trips and shuts things down - which is annoying. Especially when I'm pulling a shot and it shuts down - which happens more than I want it to.

## Mounting to the machine

TBD. The idea I have is to create a plate with magnets on either side of the sensor spaced out a bit. Then just use the magnets on glued to the plate and have corresponding magnets on the top side of the lid - should keep the sensor in place and avoids drilling into the lid

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

There will also be a calibration step. I have placeholder values - I need to get a reading when the machine reports empty and then again when I fill it back up.

Since I have the W variant I'm going to write up a web server function that I can call from my phone when I'm home - this way I can check before heading to the basement and grab the water. The W variant of the pico is so cheap why not!