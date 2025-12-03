import network
from time import sleep
from machine import Pin, PWM, I2C, SPI
import music
import utime
from mpu9250 import MPU9250
import requests
import json
import _thread
import icons
import captive 
import display

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

button1 = Pin(17,Pin.IN, Pin.PULL_UP)
button2 = Pin(16,Pin.IN, Pin.PULL_UP)
sensor = MPU9250(i2c)

def init():
    try: 
        f = open('wlan.info')
        data = f.read() 
        creds = data.split(" ")
        print(creds)
        if(not len(creds[0]) and not len(creds[1])):
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
            wlan.active(True)
            ap = network.WLAN(network.AP_IF)
            ap.active(False)
            ap.active(True)
            ap.config(essid="HabCube", password="habcube2115")
            captive.start(ap,wlan)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.active(True) 
        wlan.connect(creds[0], creds[1])
        connection_timeout = 10
        while( connection_timeout > 0):
            if wlan.isconnected():
                load_active_habits()
                break
            else:
                display.display_text_centered("Trying connecting to wifi...")
                print("not connected")
                connection_timeout -= 1
                sleep(1)
        if connection_timeout <=0:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(False)
            wlan.active(True)
            ap = network.WLAN(network.AP_IF)
            ap.active(False)
            ap.active(True)
            ap.config(essid="HabCube", password="habcube2115") 
            captive.start(ap,wlan)
    except OSError:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        wlan.active(True)
        ap = network.WLAN(network.AP_IF)
        ap.active(False)
        ap.active(True)
        ap.config(essid="HabCube", password="habcube2115")
        captive.start(ap,wlan)

    load_active_habits() 
    
    display.display_active_habit(active_habits,active_habit_index)
active_habits = [] 

def load_active_habits():
    global active_habits
    response = requests.get("https://backend-1089871134307.europe-west1.run.app/api/v1/habits/active")
    content = response.content
    habits = json.loads(content)
    active_habits = habits["habits"]
    
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
        display.play_animation()


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


def loop():
    global gyro_offset_z, angle_z, last_time
    
    gyro_offset_raw = calibrate_gyro() 
    
    angle_z = 0.0
    last_time = utime.ticks_ms()

    while True:
        if(button1.value() == 0 and button2.value() == 0):
            display.show_loading_screen()
            load_active_habits() 
            display.display_active_habit(active_habits,active_habit_index)
            angle_z = 0
        elif (button1.value() == 0):
            switch_previous_habit()
            display.display_active_habit(active_habits, active_habit_index)
            utime.sleep_ms(100)
            angle_z = 0
        elif (button2.value() == 0):
            switch_next_habit()
            display.display_active_habit(active_habits, active_habit_index)
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

            complete_and_switch_habit()

            display.display_active_habit(active_habits, active_habit_index)

            angle_z = 0.0
            utime.sleep_ms(1000) 
            last_time = utime.ticks_ms() 

        utime.sleep_ms(10)
init()
loop()
