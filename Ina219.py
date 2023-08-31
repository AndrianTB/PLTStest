import board
import busio
import adafruit_ina219

i2c_bus = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c_bus)

print("Power: {:.2f} mW".format(ina219.power))
