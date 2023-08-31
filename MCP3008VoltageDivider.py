from gpiozero import MCP3008
import time

# Konfigurasi MCP3008
mcp3008 = MCP3008(channel=1)  # Saluran ADC MCP3008 yang terhubung

# Konfigurasi voltage divider
voltage_in = 3.3  # Tegangan input pada voltage divider (misalnya 3.3V)
voltage_divider_ratio = 5  # Rasio pembagi tegangan voltage divider (misalnya 2:1)

# Fungsi untuk mengukur tegangan
def measure_voltage():
    adc_value = mcp3008.value  # Membaca nilai ADC dari MCP3008
    print (adc_value)
    voltage_adc = adc_value * voltage_in  # Menghitung tegangan ADC yang dibaca
    voltage_input = voltage_adc * voltage_divider_ratio  # Menghitung tegangan input sesungguhnya
    
    return voltage_input

# Loop pengukuran tegangan
while True:
    voltage = measure_voltage()
    print("Tegangan adalah {:.2f}V".format(voltage))
    time.sleep(1)
