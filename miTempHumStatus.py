#!/usr/bin/env python3
import binascii
import base64
import requests
from bluepy.btle import UUID, Peripheral, ADDR_TYPE_PUBLIC, DefaultDelegate

# domoticz configuration
DOMOTICZ_SERVER   = "127.0.0.1:8080"
DOMOTICZ_USERNAME = ""
DOMOTICZ_PASSWORD = ""

# connection attemp number before send error
N = 5

# sensor dictionary to add own sensors
# key is MAC of BT sensor, value is sensor ID
sensor_dict = {}
sensor_dict["00:00:00:00:00:00"] = 99

# constants for polling sensor; do not change!
BATTERY_HANDLE = 0x0018
TEMP_HUM_WRITE_HANDLE = 0x0010
TEMP_HUM_READ_HANDLE = 0x000E
TEMP_HUM_WRITE_VALUE = bytearray([0x01, 0x10])

battery_level = -1
sensor_id = -1

class TempHumDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        if (cHandle == TEMP_HUM_READ_HANDLE):
            #data
            #b'T=25.1 H=40.4\x00'
            data = str(data).replace('b\'', '').replace('\\x00\'', '')
            splitted = data.split(" ")
            temperature = splitted[0][2:]
            humidity = splitted[1][2:]
            comfort_type = get_comfort_type(humidity)
            if (sensor_id != -1 and battery_level > -1):
                request_url = 'http://' + DOMOTICZ_SERVER + '/json.htm?type=command&param=udevice&idx=' + str(sensor_id) + '&nvalue=0&svalue=' + temperature + ';' + humidity + ';' + comfort_type + '&battery=' + str(battery_level)
                send_to_domoticz(request_url)

def send_to_domoticz(url):
    if (DOMOTICZ_USERNAME and DOMOTICZ_PASSWORD):
        requests.get(url, auth=(DOMOTICZ_USERNAME, DOMOTICZ_PASSWORD))
    else:
        requests.get(url)

def get_comfort_type(humidity):
    comfort_type = "0"
    if float(humidity) < 40:
        comfort_type = "2"
    elif float(humidity) <= 70:
        comfort_type = "1"
    elif float(humidity) > 70:
        comfort_type = "3"
    return comfort_type

def get_battery_value():
    battery_value = 0;
    try:
        battery_value = p.readCharacteristic(BATTERY_HANDLE)
    finally:
        return int(binascii.b2a_hex(battery_value), 16)

def handle_temp_hum_value():
    p.writeCharacteristic(TEMP_HUM_WRITE_HANDLE, TEMP_HUM_WRITE_VALUE)
    while True:
        if p.waitForNotifications(1.0):
            break

for key, value in sensor_dict.items():
    attemp_no = 0
    while attemp_no < N:
        try:
            sensor_id = value
            p = Peripheral(key)
            p.withDelegate(TempHumDelegate())
            battery_level = get_battery_value()
            handle_temp_hum_value()
            p.disconnect()
        except Exception as e:
            attemp_no += 1
            print("Attemp number " + str(attemp_no) + " from " + str(N) + " for device " + key + " gives an exception: \"" + str(e) + "\".")
            if attemp_no == N:
                n_attempts_failed_message = "miTempHum handle", "All " + str(N) + " connection attempts for device " + key + " gives an error, last was: \"" + str(e) + "\"."
                print(n_attempts_failed_message)
            pass
        else:
            break