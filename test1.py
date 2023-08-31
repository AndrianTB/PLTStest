import board
import busio
import adafruit_ina219
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
from gpiozero import OutputDevice
from time import sleep
from ubidots import ApiClient

# Initialize INA219 sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c_bus)

# Initialize Modbus RTU connection
serial_port = '/dev/ttyUSB0'
serial = serial.Serial(
    port=serial_port,
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    xonxoff=0
)
master = modbus_rtu.RtuMaster(serial)
master.set_timeout(2.0)
master.set_verbose(True)

# Initialize relays
relay_pin_1 = 17
relay_pin_2 = 18
relay1 = OutputDevice(relay_pin_1, active_high=False, initial_value=False)
relay2 = OutputDevice(relay_pin_2, active_high=False, initial_value=False)

# Ubidots API configuration
API_token = "BBFF-qOvq1tT7Z0eXXlxPg8tV0ZXimKLX3y"
api = ApiClient(token=API_token)

# Ubidots Variable IDs for Threshold Value
threshold_variable_id = "64f02bdae57b850bf9f06e0c"  # Replace with threshold variable ID

def get_threshold_value():
    threshold_variable = api.get_variable(threshold_variable_id)
    threshold_value = threshold_variable.get_values(1)[0]['value']
    return threshold_value

def send_data_to_ubidots():
    try:
        # INA219 Sensor Readings
        bus_voltage = ina219.bus_voltage
        shunt_voltage = ina219.shunt_voltage / 1000
        current = ina219.current
        power = ina219.power

        # Modbus Readings
        modbus_data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
        power_value = (modbus_data[3] + (modbus_data[4] << 16)) / 10.0

        # Get Threshold Value from Ubidots
        threshold_value = get_threshold_value()

        # Relay Control
        print("Turning on Relay 1")
        relay1.on()
        sleep(2)
        print("Turning off Relay 1")
        relay1.off()

        print("Turning on Relay 2")
        relay2.on()
        sleep(2)
        print("Turning off Relay 2")
        relay2.off()

        # Determine Power Source
        if power > threshold_value:
            power_source = "PLTS"
        else:
            power_source = "PLN"

        # Send data to Ubidots
        input_solar = api.get_variable("64f02b252249d82468f5de32")  # Replace with variable ID
        input_solar.save_value({"value": power, "context": {"power_source": power_source}})

        output_daya = api.get_variable("64f02bb9a49ebd241836bce7")  # Replace with variable ID
        output_daya.save_value({"value": power_value})

    except Exception as e:
        print("Error:", e)

try:
    while True:
        send_data_to_ubidots()
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    master.close()
