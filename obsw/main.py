import network
from time import sleep
from machine import Pin, PWM, I2C, SPI
import music
import utime
from mpu9250 import MPU9250
from sh1106 import SH1106_SPI
import framebuf
import requests
import json
import _thread
import icons
import gc
from captive_portal import CaptivePortal

gyro_offset_z = 0
angle_z = 0
last_time = 0 
icons.configure_icons()

HOW_MANY_ANIMATION_PLAY = 5
active_habit_index = 0 
active_habits = []

buzzer = PWM(Pin(22))
buzzer.duty_u16(0)
i2c = I2C(0,sda=Pin(0),scl=Pin(1))
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

button1 = Pin(17,Pin.IN, Pin.PULL_UP)
button2 = Pin(16,Pin.IN, Pin.PULL_UP)
sensor = MPU9250(i2c)
def init():

    # portal = CaptivePortal()

    # creds = portal.start()

    # crashing later when sending request


    # wlan = network.WLAN(network.STA_IF)
    # wlan.active(True)
    # wlan.connect(creds.ssid, creds.password)
    
    # connection_timeout = 10
    # while connection_timeout > 0:
    #     if wlan.status() >= 3:
    #         break
    #     connection_timeout -= 1
    #     print('Waiting for Wi-Fi connection...')
    #     sleep(1)

    # if wlan.status() != 3:
    #     raise RuntimeError('Failed to establish a network connection')
    # else:
    #     print('Connection successful!')
    #     network_info = wlan.ifconfig()
    #     print('IP address:', network_info[0])


    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(wlan.scan())

    ssid = 'Tenda_8CE3B0'
    password = 'everycake306'

    wlan.connect(ssid, password)

    connection_timeout = 100
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Failed to establish a network connection')
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])

    load_active_habits() 
    
    display_active_habit()

def load_active_habits():
    global active_habits
    print("test")
    response = requests.get("https://backend-1089871134307.europe-west1.run.app/api/v1/habits/active")
    print(response)
    content = response.content
    habits = json.loads(content)
    active_habits = habits["habits"]

def play_animation(display1,display2, frame_delay_ms=5):
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
                        
                        display1.fill(0)
                        display1.blit(fb, 0, 0)
                        display1.show()

                        display2.fill(0)
                        display2.blit(fb, 0, 0)
                        display2.show()
                        
                        utime.sleep_ms(frame_delay_ms)
                        frame_number += 1

            except OSError:
                if frame_number == 1:
                    print(f"End Animation")
                else:
                    print("End animation")
                break
    
def calibrate_gyro(samples=200):
    print("Calibrate gyroscope...")
    sum_z = 0
    for _ in range(samples):
        sum_z += sensor.gyro[2]
        utime.sleep_ms(5)
    offset_z = sum_z / samples
    print(f"Calibrated gyroscope. Offset Z: {offset_z}")
    return offset_z  

def play_sui_animation():
    for _ in range(0,5):
        play_animation(display_oled1,display_oled2)

def display_active_habit():
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

def complete_and_switch_habit():
    response = requests.post(f"https://backend-1089871134307.europe-west1.run.app/api/v1/habits/{str(active_habits[active_habit_index]["id"])}/complete",json={})
    print(response.content) 
    if (response.status_code == 200):
        active_habits.pop(active_habit_index)
        switch_next_habit()

def switch_next_habit():
    global active_habit_index
    active_habit_index += 1
    if(active_habit_index >= len(active_habits)):
        active_habit_index = 0

def switch_previous_habit():
    global active_habit_index
    active_habit_index -= 1
    if(active_habit_index < 0):
        active_habit_index = len(active_habits) - 1 

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

def loop():
    global gyro_offset_z, angle_z, last_time
    
    gyro_offset_raw = calibrate_gyro() 
    
    angle_z = 0.0
    last_time = utime.ticks_ms()

    while True:
        if(button1.value() == 0 and button2.value() == 0):
            show_loading_screen()
            load_active_habits() 
            display_active_habit()
            angle_z = 0
        elif (button1.value() == 0):
            switch_previous_habit()
            display_active_habit()
            utime.sleep_ms(100)
            angle_z = 0
        elif (button2.value() == 0):
            switch_next_habit()
            display_active_habit()
            utime.sleep_ms(100)
            angle_z = 0

        
        current_time = utime.ticks_ms()
        dt = utime.ticks_diff(current_time, last_time) / 1000.0 
        last_time = current_time

        gyro_z_raw = sensor.gyro[2]
        
        gyro_z_rad = gyro_z_raw - gyro_offset_raw
        
        gyro_z_deg = gyro_z_rad * 57.296


        if abs(gyro_z_deg) < 0.5:
            gyro_z_deg = 0

        angle_z += gyro_z_deg * dt

        if abs(angle_z) >= 160:        
            print("Rotation!")
            
            _thread.start_new_thread(music.play_mario_main_theme,(buzzer,))
            play_sui_animation()

            # complete_and_switch_habit()

            display_active_habit()

            angle_z = 0.0
            utime.sleep_ms(1000) 
            last_time = utime.ticks_ms() 

        utime.sleep_ms(10)
init()
loop()