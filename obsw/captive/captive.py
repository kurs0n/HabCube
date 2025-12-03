import socket
import time
import machine
import display
def fetch_networks(wlan):
    scan_results = wlan.scan()
    found_ssids = set()
    ssid_options = ""
    for result in scan_results:
        ssid = result[0].decode('utf-8')
        if ssid and ssid not in found_ssids:
            found_ssids.add(ssid)
            ssid_options += '<option value="{}">{}</option>'.format(ssid, ssid)
    return ssid_options    

def start(ap, wlan):
    display.display_text_centered("Hotspot Created")
    ip=ap.ifconfig()[0]

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
                            display.display_text_centered("Connecting to wifi...")
                            print("Trying to connect")
                            connection_timeout -= 1
                            time.sleep(1)
                    if not wlan.isconnected():
                        display.display_text_centered("Wrong Credentials!")
                        print("Wrong credentials!")

                ssid_options = fetch_networks(wlan)
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