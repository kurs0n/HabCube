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
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ssid = b"Patryk\xe2\x80\x99s iPhone"
    password = 'marcela2115'

    wlan.connect(ssid, password)

    connection_timeout = 10
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

    calibrate_gyro()

def load_active_habits():
    response = requests.get("https://backend-1089871134307.europe-west1.run.app/api/v1/habits")
    content = response.content
    habits = json.loads(content)
    for habit in habits["habits"]:
        if(habit["active"]):
            active_habits.append(habit)

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
                        
                        print(f"Displayed frame: {filename}")
                        
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
    display_oled1.fill(1)
    display_oled2.fill(1)
    display_oled1.text(habit_name,25,28,0)
    display_oled2.text(habit_name,25,28,0)
    display_oled1.show()    
    display_oled2.show()

def switch_next_habit():
    return None

def switch_previous_habit():
    
    return None

def loop():
    gyro_offset_z = calibrate_gyro()
    angle_z = 0.0
    last_time = utime.ticks_ms()

    while(True):
        current_time = utime.ticks_ms()
        delta_t = utime.ticks_diff(current_time, last_time) / 1000.0 
        last_time = current_time

        gyro_z_velocity = sensor.gyro[2] - gyro_offset_z
        
        angle_z += gyro_z_velocity * delta_t

        if abs(angle_z) >= 0.55:        
            
            mario_theme_thread = _thread.start_new_thread(music.play_mario_main_theme,(buzzer)) # thread is not working at all
            play_sui_animation()
        
            # switch habit and complete current one
            
            # display_active_habit()

            angle_z = 0.0
            
            utime.sleep_ms(1000)

        utime.sleep_ms(20)        
init()
loop()