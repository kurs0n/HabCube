# import network
# from time import sleep
# from machine import Pin, PWM, I2C, SPI
# import music
# import utime
# from mpu9250 import MPU9250
# from sh1106 import SH1106_SPI
# import framebuf
# import requests
# import json
# import _thread
# import icons

# gyro_offset_z = 0
# angle_z = 0
# last_time = 0 
# icons.configure_icons()

# HOW_MANY_ANIMATION_PLAY = 5
# active_habit_index = 0 
# active_habits = []

# buzzer = PWM(Pin(22))
# buzzer.duty_u16(0)
# i2c = I2C(0,sda=Pin(0),scl=Pin(1))
# spi_oled1 = SPI(0, baudrate=1000000, sck=Pin(2),mosi=Pin(3))
# cs_oled1 = Pin(4, Pin.OUT, value=1)   
# dc_oled1 = Pin(5, Pin.OUT)
# rst_oled1 = Pin(6, Pin.OUT)

# spi_oled2 = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11))
# cs_oled2 = Pin(12,  Pin.OUT, value=1)
# dc_oled2 = Pin(13, Pin.OUT)
# rst_oled2 = Pin(9, Pin.OUT)

# display_oled1 = SH1106_SPI(128, 64, spi_oled1, dc_oled1, rst_oled1, cs_oled1, rotate=0, delay=0)   
# display_oled2 = SH1106_SPI(128, 64, spi_oled2, dc_oled2, rst_oled2, cs_oled2, rotate=0, delay=0)

# button1 = Pin(17,Pin.IN, Pin.PULL_UP)
# button2 = Pin(16,Pin.IN, Pin.PULL_UP)
# sensor = MPU9250(i2c)
# def init():

#     # portal = CaptivePortal()

#     # creds = portal.start()

#     # wlan = network.WLAN(network.STA_IF)
#     # wlan.active(True)
#     # wlan.connect(creds.ssid, creds.password)
    
#     # connection_timeout = 10
#     # while connection_timeout > 0:
#     #     if wlan.status() >= 3:
#     #         break
#     #     connection_timeout -= 1
#     #     print('Waiting for Wi-Fi connection...')
#     #     sleep(1)

#     # if wlan.status() != 3:
#     #     raise RuntimeError('Failed to establish a network connection')
#     # else:
#     #     print('Connection successful!')
#     #     network_info = wlan.ifconfig()
#     #     print('IP address:', network_info[0])


#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     print(wlan.scan())

#     ssid = 'Czarnuch'
#     password = 'marcela2115'

#     wlan.connect(ssid, password)

#     connection_timeout = 100
#     while connection_timeout > 0:
#         if wlan.status() >= 3:
#             break
#         connection_timeout -= 1
#         print('Waiting for Wi-Fi connection...')
#         sleep(1)

#     if wlan.status() != 3:
#         raise RuntimeError('Failed to establish a network connection')
#     else:
#         print('Connection successful!')
#         network_info = wlan.ifconfig()
#         print('IP address:', network_info[0])

#     load_active_habits() 
    
#     display_active_habit()
active_habits = [] 

def load_active_habits():
    global active_habits
    response = requests.get("https://backend-1089871134307.europe-west1.run.app/api/v1/habits/active")
    content = response.content
    habits = json.loads(content)
    active_habits = habits["habits"]

# def play_animation(display1,display2, frame_delay_ms=5):
#     frame_number = 1
#     while True:
#             filename = f"resized_{frame_number}.bmp"
#             try:
#                 with open(filename, "rb") as f:
#                         f.seek(10)
#                         data_offset = int.from_bytes(f.read(4), "little")
#                         f.seek(data_offset)
#                         buffer = f.read()
#                         fb = framebuf.FrameBuffer(bytearray(buffer), 128, 64, framebuf.MONO_HLSB)
                        
#                         display1.fill(0)
#                         display1.blit(fb, 0, 0)
#                         display1.show()

#                         display2.fill(0)
#                         display2.blit(fb, 0, 0)
#                         display2.show()
                        
#                         utime.sleep_ms(frame_delay_ms)
#                         frame_number += 1

#             except OSError:
#                 if frame_number == 1:
#                     print(f"End Animation")
#                 else:
#                     print("End animation")
#                 break
    
# def calibrate_gyro(samples=200):
#     print("Calibrate gyroscope...")
#     sum_z = 0
#     for _ in range(samples):
#         sum_z += sensor.gyro[2]
#         utime.sleep_ms(5)
#     offset_z = sum_z / samples
#     print(f"Calibrated gyroscope. Offset Z: {offset_z}")
#     return offset_z  

# def play_sui_animation():
#     for _ in range(0,5):
#         play_animation(display_oled1,display_oled2)

# def display_active_habit():
#     habit_name = active_habits[active_habit_index]["name"]
#     display_oled1.fill(0)
#     display_oled2.fill(0)
#     x_icon = (128 - 80) // 2

#     if(active_habits[active_habit_index]["type"]== "water"):
#         display_oled1.blit(icons.fb_glass,x_icon,0)
#         display_oled2.blit(icons.fb_glass,x_icon,0)
#     elif (active_habits[active_habit_index]["type"] =="sport"):
#         display_oled1.blit(icons.fb_sport,x_icon,0)
#         display_oled2.blit(icons.fb_sport,x_icon,0)
#     elif (active_habits[active_habit_index]["type"]=="language"):
#         display_oled1.blit(icons.fb_lang,x_icon,0)
#         display_oled2.blit(icons.fb_lang,x_icon,0)
#     elif(active_habits[active_habit_index]["type"] == "read"): 
#         display_oled1.blit(icons.fb_glasses,x_icon,0)
#         display_oled2.blit(icons.fb_glasses,x_icon,0)
#     elif (active_habits[active_habit_index]["type"] == "code"):
#         display_oled1.blit(icons.fb_code,x_icon,0)
#         display_oled2.blit(icons.fb_code,x_icon,0)
    

#     text_length = len(habit_name) * 8
#     x_text = (128 - text_length) // 2
#     y_text = 52
#     if(x_text < 0):
#         x_text = 0
#     display_oled1.text(habit_name,x_text,y_text,1)
#     display_oled2.text(habit_name,x_text,y_text,1)
#     display_oled1.show()    
#     display_oled2.show()

# def complete_and_switch_habit():
#     response = requests.post(f"https://backend-1089871134307.europe-west1.run.app/api/v1/habits/{str(active_habits[active_habit_index]["id"])}/complete",json={})
#     print(response.content) 
#     if (response.status_code == 200):
#         active_habits.pop(active_habit_index)
#         switch_next_habit()

# def switch_next_habit():
#     global active_habit_index
#     active_habit_index += 1
#     if(active_habit_index >= len(active_habits)):
#         active_habit_index = 0

# def switch_previous_habit():
#     global active_habit_index
#     active_habit_index -= 1
#     if(active_habit_index < 0):
#         active_habit_index = len(active_habits) - 1 

# def show_loading_screen():
#     display_oled1.fill(0)
#     display_oled2.fill(0) 
#     text_length = len("Loading Habits...") * 8
#     x_text = (128 - text_length) // 2
#     y_text = 22
#     if(x_text < 0):
#         x_text = 0
#     display_oled1.text("Loading Habits...",x_text,y_text,1)
#     display_oled2.text("Loading Habits...",x_text,y_text,1)
#     display_oled1.show()    
#     display_oled2.show() 

# def loop():
#     global gyro_offset_z, angle_z, last_time
    
#     gyro_offset_raw = calibrate_gyro() 
    
#     angle_z = 0.0
#     last_time = utime.ticks_ms()

#     while True:
#         if(button1.value() == 0 and button2.value() == 0):
#             show_loading_screen()
#             load_active_habits() 
#             display_active_habit()
#             angle_z = 0
#         elif (button1.value() == 0):
#             switch_previous_habit()
#             display_active_habit()
#             utime.sleep_ms(100)
#             angle_z = 0
#         elif (button2.value() == 0):
#             switch_next_habit()
#             display_active_habit()
#             utime.sleep_ms(100)
#             angle_z = 0

        
#         current_time = utime.ticks_ms()
#         dt = utime.ticks_diff(current_time, last_time) / 1000.0 
#         last_time = current_time

#         gyro_z_raw = sensor.gyro[2]
        
#         gyro_z_rad = gyro_z_raw - gyro_offset_raw
        
#         gyro_z_deg = gyro_z_rad * 57.296


#         if abs(gyro_z_deg) < 0.5:
#             gyro_z_deg = 0

#         angle_z += gyro_z_deg * dt

#         if abs(angle_z) >= 160:        
#             print("Rotation!")
            
#             _thread.start_new_thread(music.play_mario_main_theme,(buzzer,))
#             play_sui_animation()

#             # complete_and_switch_habit()

#             display_active_habit()

#             angle_z = 0.0
#             utime.sleep_ms(1000) 
#             last_time = utime.ticks_ms() 

#         utime.sleep_ms(10)
# init()
# loop()


import socket
import network
import time
import machine
import requests
import json

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
wlan.active(True)

def fetch_networks():
    global wlan
    scan_results = wlan.scan()
    found_ssids = set()
    ssid_options = ""
    for result in scan_results:
        ssid = result[0].decode('utf-8')
        if ssid and ssid not in found_ssids:
            found_ssids.add(ssid)
            ssid_options += '<option value="{}">{}</option>'.format(ssid, ssid)
    return ssid_options    


ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.active(True)
ap.config(essid="HabCube", password="habcube2115")

CONTENT = b"""\
HTTP/1.0 200 OK

<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Wi-Fi Configuration</title>
    <style>
        :root {{
            --primary-color: #4a90e2;
            --bg-color: #f0f2f5;
            --card-bg: #ffffff;
            --text-color: #333;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }}
        .card {{
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }}
        h2 {{
            margin-top: 0;
            color: var(--text-color);
            text-align: center;
            font-weight: 600;
        }}
        .form-group {{
            margin-bottom: 1.2rem;
        }}
        label {{
            display: block;
            margin-bottom: 0.5rem;
            color: #666;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        select, input {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            box-sizing: border-box;
            transition: border-color 0.2s;
            background-color: #fff;
        }}
        select:focus, input:focus {{
            border-color: var(--primary-color);
            outline: none;
            box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
        }}
        button {{
            width: 100%;
            padding: 14px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }}
        button:hover {{
            background-color: #357abd;
        }}
        /* Fix for iOS removing default appearance */
        select {{
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
            background-repeat: no-repeat;
            background-position: right .7em top 50%;
            background-size: .65em auto;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Setup Wi-Fi</h2>
        <form action="/connect" method="post">

            <div class="form-group">
                <label for="ssid">Choose Network</label>
                <select name="ssid" id="ssid">
                    {}
                </select>
            </div>

            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" name="password" id="password" placeholder="Enter Wi-Fi Password">
            </div>

            <button type="submit">Connect</button>
        </form>
    </div>
</body>
</html>
"""

def start():
    global ap, wlan
    # DNS Server
    ip=ap.ifconfig()[0]

    # Web Server
    s = socket.socket()
    ai = socket.getaddrinfo(ip, 80)
    print("Web Server: Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(2)
    print("Web Server: Listening http://{}:80/".format(ip))

    counter = 0

    wlan_ssid = None
    wlan_pass = None

    try:
        while 1:
            try:
                res = s.accept()
                client_sock = res[0]

                client_stream = client_sock

                # req = client_stream.readline()

                content_length = 0
                while True:
                    h = client_stream.readline()
                    if h.startswith(b"Content-Length:"):
                        content_length = int(h.split(b":")[1].strip())
                    if h == b"" or h == b"\r\n" or h == None:
                        break

                post_data = b""
                if content_length > 0:
                    post_data = client_stream.read(content_length)
                    params = {}
                    for pair in post_data.decode().split('&'):
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            params[key] = value.replace('+', ' ')
                    print(params['ssid'],params['password'])
                    wlan.connect(params['ssid'],params['password'])
                    connection_timeout = 10
                    while connection_timeout > 0:
                        if(wlan.isconnected()):
                            ap.active(False)
                            wlan_ssid = params['ssid']
                            wlan_pass = params['password']
                            f = open('wlan.info', 'w')
                            f.write(wlan_ssid + " " + wlan_pass)
                            f.close() 
                            time.sleep(2)
                            machine.reset()
                            break
                        else:
                            print("Trying to connect")
                            connection_timeout -= 1
                            time.sleep(1)
                    if not wlan.isconnected():
                        print("Wrong credentials!")
                # request_url = req[4:-11]
                # api = request_url[:10]
                # if api == b'/connect?':
                #     print("test")
                ssid_options = fetch_networks()
                client_stream.write(CONTENT.format(ssid_options))

                client_stream.close()
                counter += 1
            except:
                pass
            if (wlan_ssid and wlan_pass):
                break
            time.sleep_ms(300)
    except KeyboardInterrupt:
        print('Closing')
    return [wlan_ssid,wlan_pass]
f = open('wlan.info')
data = f.read() 
ssid = data.split(" ")[0]
password = data.split(" ")[1] ## PICO is not ready to work in two modes ap an sta so reset the machine and later if we have a file and connect succesfully we use this if not we run as an access point pure software magic do it tomorrow 
if(not ssid and not password):
    print(start())
wlan.connect(ssid, password)
print(load_active_habits())