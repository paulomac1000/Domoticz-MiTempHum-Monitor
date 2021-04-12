# Domoticz Mi TempHum Monitor

A library written in Python that connects to Xiaomi via bluetooth and retrieves data on the current temperature, humidity and battery status of the device.

## Requirements

- `Linux` based device (like `Raspberry Pi`) with installed `Python 3` and Bluetooth Low Energy Support (Raspberry supports this standard by default, if you use a different device, you must check the manufacturer's website; remember that you can always buy an external USB module).
- Mi Bluetooth Temperature & Humidity Monitor device (the first, oval version)
- The following python packages installed on device: `requests`, `bluepy`

## Installation

### Get the MAC address of the device

You can do this in several ways:
- (easiest) use the "BLE Scanner" or similar application on your mobile device,
- use the hcitool application on your Linux device.

### Configure Domoticz

Open the Domoticz panel, expand "Setup", select "Hardware" and add a new device named "Mi TempHum Monitor", type "Dummy (Does nothing, use for virtual switches only)". Leave the rest of the options unchanged and press the "Add" button.

At the newly created item in the "Type" column, press the "Create Virtual Sensors" button. A modal will appear in which you must enter the name of the sensor "Temp & Hum" and the type "Temp + Hum".

Now go to the "Temperature" tab and click the "Edit" button on the newly created item. At the top of the open modal you have the "Idx" field - write down its value somewhere.

### Install script

Install required Python packages:

```bash
pip3 install requests bluepy
```

Clone the repository to any directory on your device, e.g. to the home directory.

```bash
cd
git clone https://github.com/paulomac1000/Domoticz-MiTempHum-Monitor
```

Change to the script's directory

```bash
cd Domoticz-MiTempHum-Monitor
```

Configure the script

```bash
nano miTempHumStatus.py
```

Go to line 8 (to the code below) and replace this url with your Domoticz url, or leave the default configuration if the script is run on the same machine.

```python
DOMOTICZ_SERVER = "127.0.0.1:8080"
```

Go to line 18 (to the code below)  and replace the value in square brackets with the MAC address of your device and change the value after the equal sign to Idx of the added sensor in Domoticz. In the following lines, you can add the configuration of other devices in the same way, if you have any.

```python
sensor_dict["00:00:00:00:00:00"] = 99
```

Close the file with `ctrl+x` and save changes.

## Usage

To run a script, run it from the command line.

```bash
python3 miTempHumStatus.py
```

For the script to run automatically, add it to the `crontab`.

```bash
crontab -e
```

And call script. The following command will run the script every 15 minutes.

```bash
*/15 * * * * python3 /home/pi/Domoticz-MiTempHum-Monitor/miTempHumStatus.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Show your support

Please star this repository if this project helped you!

## Thanks
Thanks to fr31b3u73r who made the first version of the script [miThermoHygro](https://github.com/fr31b3u73r/miThermoHygro) (in Python 2). His script doesn't work anymore, but based on his work, I fixed bugs and extended its functionality.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## See also
Blog post on [cleverblog.pl](https://cleverblog.pl/?p=204)