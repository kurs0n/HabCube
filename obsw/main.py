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
    control_byte = (1 << 3)
    i2c.writeto(0x70,bytes([control_byte]))
    spi = SPI(0, baudrate=1000000)
    cs = Pin(4, Pin.OUT, value=1)
    dc = Pin(5, Pin.OUT)
    rst = Pin(6, Pin.OUT)

    display = SH1106_SPI(128, 64, spi, dc, rst, cs, rotate=0, delay=0)   
    display.sleep(False)
    display.fill(0)
    # display.text("piotrek ziobrowski śmierdzi gównem",0,0,1)
    display.text("piotrek ziobrow",0,0,1)
    display.show()
    sleep(4)
    display.fill(0)
    display.show()
    display.text("-ski smierdzi go",0,0,1)
    display.show()
    sleep(4)
    display.fill(0)
    display.show()
    display.text("-wnem",0,0,1)
    display.show()
    # i2c.writeto(0x70, bytes([1 << 3])) # enable 3 bus on multiplexer
    # i2c.writeto(0x70, bytes([1 << 0])) # ekrany są zlutownae na SPI!
    sensor = MPU9250(i2c)
    print(hex(sensor.whoami))
    while(True):
        print(sensor.acceleration) # (X,Y,Z)
        utime.sleep_ms(1000)
        music.play_mario_main_theme(buzzer)


init()
loop()