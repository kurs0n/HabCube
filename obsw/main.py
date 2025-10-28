import network
from time import sleep
from machine import Pin, PWM, I2C, SPI
import music
import utime
from mpu9250 import MPU9250
from sh1106 import SH1106_SPI

buzzer = PWM(Pin(22))
buzzer.duty_u16(0)

def init():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ssid = 'Tenda_8CE3B0'
    password = 'everycake306'

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

def loop():
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
    display_oled2.sleep(False)
    display_oled2.fill(0)
    display_oled2.text('test', 0, 0, 1)
    display_oled2.show()

    display_oled1.sleep(False)
    display_oled1.fill(0)
    display_oled1.text('piotr ziobro', 0, 0, 1)
    display_oled1.show()
   
    sensor = MPU9250(i2c)
    print(hex(sensor.whoami))
    while(True):
        print(sensor.acceleration) # (X,Y,Z)
        utime.sleep_ms(1000)
        # music.play_mario_main_theme(buzzer)

init()
loop()