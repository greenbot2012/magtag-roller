import time
import random
from adafruit_magtag.magtag import MagTag
import math
magtag = MagTag()
rolled=False
roll=0
die_no=5
die_names=["D4","D6","D8","D10","D12","D20"]
die_sides=[4,6,8,10,12,20]
magtag.graphics.set_background("/boot_screen.bmp")
magtag.refresh()
time.sleep(1)
magtag.peripherals.play_tone(1047,0.1)
magtag.peripherals.play_tone(1318,0.1)
magtag.peripherals.play_tone(1568,0.1)
time.sleep(5)
def setup_screen():
    magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
    )
    magtag.add_text(
    text_position=(
        2,
        7,
    ),
    text_scale=2,
    )
def update_screen():

    if rolled:
       magtag.set_text(str(roll),0,False)
    else:
        magtag.set_text(die_names[die_no],0,False)
    magtag.set_text(str(get_battery_percent())+"%",1,False)
    magtag.refresh()
    #magtag.peripherals.play_tone(1000,0.1)
def get_battery_percent(voltage=magtag.peripherals.battery):
    voltage=voltage or magtag.peripherals.battery
    """
    Converts LiPo voltage to a percentage for the Adafruit MagTag.
    Assumes 3.2V is 0% and 4.2V is 100%.
    """
    # Define our voltage range
    v_min = 3.2
    v_max = 4.2
    
    # Calculate percentage
    percentage = (voltage - v_min) / (v_max - v_min) * 100
    
    # Clamp the value between 0 and 100
    return math.floor(max(0, min(100, percentage))+0.5)
setup_screen()
update_screen()
button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)
magtag.peripherals.neopixels.fill(button_colors[1])

while True:
    if magtag.peripherals.button_c_pressed:
        rolled=True
        roll=random.randint(1,die_sides[die_no])
        magtag.peripherals.neopixels.fill(button_colors[2])
        update_screen()
    elif magtag.peripherals.button_b_pressed:
        rolled=False
        roll=0
        update_screen()
        magtag.peripherals.neopixels.fill(button_colors[1])
    elif magtag.peripherals.button_a_pressed and not rolled:
        if die_no == 0:
            die_no=5
        else:
            die_no-=1
        update_screen()
    elif magtag.peripherals.button_d_pressed and not rolled:
        if die_no == 5:
            die_no=0
        else:
            die_no+=1
        update_screen()
        
    
    #time.sleep(0.001)
