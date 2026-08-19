from machine import ADC
from time import sleep

TEMP_SENSOR = 4

temp_sensor = ADC(TEMP_SENSOR)

while True:
    temp_adc_value = temp_sensor.read_u16()  # read 16 bit ADC value
    temp_adc_voltage = temp_adc_value / 65535 * 3.3  # max 16 bit value * max/supply voltage
    temperature = 27 - (temp_adc_voltage - 0.706) / 0.001721  # as documented in datasheet
    print("{: 6}: {:.3f}V -> {:.1f}°C".format(temp_adc_value, temp_adc_voltage, temperature))
    sleep(1)


    
    
