# Importing necessary libraries
from machine import Pin
import time
import rp2
import network
import ubinascii
import urequests as requests
import socket
from sys import *

# HTML page for remote control which will be replaced by an application
html = """
<!DOCTYPE html>
<!-- HTML Structure for Remote Control -->
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>My Candle</title>
  </head>
  <body>
    <!-- Navigation Bar with Logo -->
    <nav>
      <img src="./medias/Mycandle.png" alt="My candle logo" />
    </nav>

    <!-- Candle Control Section -->
    <section class="card">
      <div class="candleCard">
        <!-- Left Section with Image and Description -->
        <div class="left">
          <img
            src="./medias/Capture d’écran 2023-10-11 à 10.44.11.png"
            alt=""
          />
          <p>Bougie salle de classe</p>
        </div>
        <!-- Button Section for ON and OFF -->
        <div class="button">
          <a href=\"?led=on\"><button>ON</button></a>
          <a href=\"?led=off\"><button class="red">OFF</button></a>
        </div>
      </div>
    </section>

    <!-- CSS Styling for the HTML Page -->
    <style>
    body {
      border: 0;
      margin: 1% 2% 0 2%;
      padding: 0;
    }
    
    nav img {
      width: 200px;
    }
    
    .candleCard {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0px 0px 6px 3px rgba(130, 130, 130, 0.25);
      margin-top: 5%;
    }
    .candleCard .left {
      display: flex;
      gap: 30px;
      align-items: center;
    }
    .candleCard .left img {
      width: 40px;
      margin-bottom: 10px;
    }
    .candleCard .left p {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 25px;
    }
    .candleCard .button {
      display: flex;
      gap: 10px;
    }
    .candleCard .button button {
      border-radius: 10px;
      box-shadow: 0px 0px 6px 3px rgba(130, 130, 130, 0.25);
      background-color: rgb(248, 248, 248);
      border: 1px solid rgb(209, 209, 209);
      width: 80px;
      height: 30px;
    }
    .candleCard .button .red:hover {
      background-color: #ff3b31;
    }
    .candleCard .button button:hover {
      cursor: pointer;
      background-color: #17c571;
      color: white;
      transition: 0.2s;
    }
    
    /*# sourceMappingURL=style.css.map */
    </style>
  </body>
</html>
"""

# Set country for WiFi
rp2.country('FR')

# WiFi credentials
ssid = 'reseau'  # replace with your network name
pw = '00000000'  # replace with your network password

# Activate WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Get MAC address
mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
print('mac = ' + mac)

# Connect to WiFi
ssid = ssid
pw = pw
wlan.connect(ssid, pw)

# Wait for WiFi connection
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    time.sleep(1)

# Define blinking function for onboard LED to indicate error codes
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)

# Get WiFi connection status
wlan_status = wlan.status()
blink_onboard_led(wlan_status)

# Raise an error if WiFi connection fails
if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    status = wlan.ifconfig()
    print('ip = ' + status[0])

# Function to load HTML page
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# Define GPIO pins
led = machine.Pin('LED', machine.Pin.OUT)

# ______________________________________________________________
# Program

# Define GPIO pins for various components
button = Pin(22, Pin.IN, Pin.PULL_UP)
pir = Pin(15, Pin.IN, Pin.PULL_DOWN)
ventilo = machine.Pin(16, machine.Pin.OUT)
arc = machine.Pin(21, machine.Pin.OUT)

# Define GPIO pins for stepper motor
motor_GP = [0, 1, 2, 3]
seq_pointer = [0, 1, 2, 3, 4, 5, 6, 7]
stepper_obj = []

# Define stepper motor sequence
arrSeq = [[0, 0, 0, 1], \
          [0, 0, 1, 1], \
          [0, 0, 1, 0], \
          [0, 1, 1, 0], \
          [0, 1, 0, 0], \
          [1, 1, 0, 0], \
          [1, 0, 0, 0], \
          [1, 0, 0, 1]]

# Initialize stepper motor pins
for gp in motor_GP: stepper_obj.append(Pin(gp, Pin.OUT))

# Function to move stepper motor
def stepper_move(direction):  # direction must be +1 or -1
    global seq_pointer
    seq_pointer = seq_pointer[direction:] + seq_pointer[:direction]
    for a in range(4): stepper_obj[a].value(arrSeq[seq_pointer[0]][a])
    sleep(0.001)

# Function to turn on the candle
def allumage():
    arc.value(1)
    time.sleep(3)
    arc.value(0)

# Function to turn off the candle
def extinction():
    ventilo.value(1)
    time.sleep(5)
    ventilo.value(0)

# Main loop
while True:
    try:
        cl, addr = s.accept()
        r = cl.recv(1024)

        # Extract the command from the HTTP request
        r = str(r)
        led_on = r.find('?led=on')
        led_off = r.find('?led=off')

        # Process the command
        if led_on > -1:
            if led_on > -1:
                # Perform a sequence of actions based on button, PIR sensor, and stepper motor
                while button.value() == 1:
                    stepper_move(-1)
                while button.value() == 0:
                    stepper_move(1)
                    pass
                while pir.value() == 0:
                    stepper_move(1)
                while pir.value() == 1:
                    stepper_move(0)
                    time.sleep(2)
                    allumage()
                    break
                while button.value() == 1:
                    stepper_move(-1)
                while button.value() == 0:
                    stepper_move(0)
                    time.sleep(10)
                    pass
                while pir.value() == 0:
                    stepper_move(1)
                while pir.value() == 1:
                    stepper_move(0)
                    time.sleep(2)
                    extinction()
                    time.sleep(15)

        if led_off > -1:
            # Turn off the candle
            extinction()
            exit()

        # Send the HTML response
        response = html
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
