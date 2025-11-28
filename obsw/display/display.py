from machine import Pin, PWM, I2C, SPI
from sh1106 import SH1106_SPI
import icons
import framebuf
import utime 
spi_oled1 = SPI(0, baudrate=1000000, sck=Pin(2),mosi=Pin(3))
cs_oled1 = Pin(4, Pin.OUT, value=1)   
dc_oled1 = Pin(5, Pin.OUT)
rst_oled1 = Pin(6, Pin.OUT)

spi_oled2 = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11))
cs_oled2 = Pin(12,  Pin.OUT, value=1)
dc_oled2 = Pin(13, Pin.OUT)
rst_oled2 = Pin(9, Pin.OUT)

display_oled1 = SH1106_SPI(128, 64, spi_oled1, dc_oled1, rst_oled1, cs_oled1, rotate=0, delay=0)   
display_oled2 = SH1106_SPI(128, 64, spi_oled2, dc_oled2, rst_oled2, cs_oled2, rotate=0, delay=0)

def display_text_centered(text):
    global display_oled1,display_oled2
    display_oled1.fill(0)
    display_oled2.fill(0)

    text_length = len(text) * 8
    x_text = (128 - text_length) // 2
    y_text = 28
    if(x_text < 0):
        x_text = 0

    display_oled1.text(text, x_text, y_text, 1)
    display_oled2.text(text, x_text, y_text, 1)
    display_oled1.show()
    display_oled2.show()

def display_active_habit(active_habits,active_habit_index):
    habit_name = active_habits[active_habit_index]["name"]
    display_oled1.fill(0)
    display_oled2.fill(0)
    x_icon = (128 - 80) // 2

    if(active_habits[active_habit_index]["type"]== "water"):
        display_oled1.blit(icons.fb_glass,x_icon,0)
        display_oled2.blit(icons.fb_glass,x_icon,0)
    elif (active_habits[active_habit_index]["type"] =="sport"):
        display_oled1.blit(icons.fb_sport,x_icon,0)
        display_oled2.blit(icons.fb_sport,x_icon,0)
    elif (active_habits[active_habit_index]["type"]=="language"):
        display_oled1.blit(icons.fb_lang,x_icon,0)
        display_oled2.blit(icons.fb_lang,x_icon,0)
    elif(active_habits[active_habit_index]["type"] == "read"): 
        display_oled1.blit(icons.fb_glasses,x_icon,0)
        display_oled2.blit(icons.fb_glasses,x_icon,0)
    elif (active_habits[active_habit_index]["type"] == "code"):
        display_oled1.blit(icons.fb_code,x_icon,0)
        display_oled2.blit(icons.fb_code,x_icon,0)
    

    text_length = len(habit_name) * 8
    x_text = (128 - text_length) // 2
    y_text = 52
    if(x_text < 0):
        x_text = 0
    display_oled1.text(habit_name,x_text,y_text,1)
    display_oled2.text(habit_name,x_text,y_text,1)
    display_oled1.show()    
    display_oled2.show()

def show_loading_screen():
    display_oled1.fill(0)
    display_oled2.fill(0) 
    text_length = len("Loading Habits...") * 8
    x_text = (128 - text_length) // 2
    y_text = 22
    if(x_text < 0):
        x_text = 0
    display_oled1.text("Loading Habits...",x_text,y_text,1)
    display_oled2.text("Loading Habits...",x_text,y_text,1)
    display_oled1.show()    
    display_oled2.show()

def play_animation(frame_delay_ms=5):
    global display_oled1,display_oled2
    frame_number = 1
    while True:
            filename = f"resized_{frame_number}.bmp"
            try:
                with open(filename, "rb") as f:
                        f.seek(10)
                        data_offset = int.from_bytes(f.read(4), "little")
                        f.seek(data_offset)
                        buffer = f.read()
                        fb = framebuf.FrameBuffer(bytearray(buffer), 128, 64, framebuf.MONO_HLSB)
                        
                        display_oled1.fill(0)
                        display_oled1.blit(fb, 0, 0)
                        display_oled1.show()

                        display_oled2.fill(0)
                        display_oled2.blit(fb, 0, 0)
                        display_oled2.show()
                        
                        utime.sleep_ms(frame_delay_ms)
                        frame_number += 1

            except OSError:
                if frame_number == 1:
                    print(f"End Animation")
                else:
                    print("End animation")
                break 