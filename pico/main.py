import time
from machine import Pin,PWM, ADC
import network
import urequests


WIFI_SSID = "S24 FE"
WIFI_PASSWORD = "password"

SERVER_IP_URL = "http://10.64.61.247:8000/"


servo1 = PWM(Pin(17))
servo1.freq(50)

min_time = 500000
max_time = 2500000

last_feed_time = 0

DEFAULT_INTERVAL = 5 * 60 * 60   # 5 hours (in seconds)
DEFAULT_ANGLE = 40
DEFAULT_DELAY = 5

wifi_status = False


def servo1_move(angle):
    duty = angle / 180 * (max_time - min_time) + min_time
    servo1.duty_ns(int(duty))


def connect_wifi():
    global wifi_status

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wifi_status = True
        print("WiFi connected:", wlan.ifconfig()[0])
        return

    print("Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    timeout = 5
    while timeout > 0 and not wlan.isconnected():
        print("Waiting for connection...")
        time.sleep(1)
        timeout -= 1

    wifi_status = wlan.isconnected()

    if wifi_status:
        print("WiFi connected:", wlan.ifconfig()[0])
    else:
        print("WiFi failed")
     

def servo_off():
    servo1_move(0)

        
def servo_on(angle, delay):
    servo1_move(angle)
    time.sleep(delay)
    servo_off()
    

def get_data():

    url = SERVER_IP_URL + "send-relay/"
    
    try:
        r = urequests.get(url)
        data = r.json()
        r.close()
        print(data)
        return data

    except Exception as e:
        print("Get error:", e)
        return {"status": False}
            
def main():
    while True:
        if not wifi_status:
            connect_wifi()
            
        if wifi_status:
            data = get_data()
            status = data.get("status")
            
            if status:
                open_delay = data.get("open_delay")
                servo_angle = data.get("servo_angle")
                
                servo_on(servo_angle, open_delay)
                
        else:            
            global last_feed_time

            now = time.time()

            if now - last_feed_time >= DEFAULT_INTERVAL:
                print("Offline feeding triggered")

                servo_on(DEFAULT_ANGLE, DEFAULT_DELAY)
                
                last_feed_time = now

        time.sleep(1)

main()


