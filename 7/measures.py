import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


dac = [8, 11, 7, 1, 0, 5, 12, 6]
dac_values = [0, 0, 0, 0, 0, 0, 0, 0]

leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in format (value, '08b')]

def bin2dec(dac_values):
    return int("".join(map(str, dac_values)), 2)

def volt():
    GPIO.input(dac, dac_values)
    return bin2dec(dac_values) / 255 * 3.3

def charging():
    GPIO.output(troyka, 1)
        
def adc_voltage():
    value = 0
    for i in range(7,-1, -1):
        GPIO.output(dac, dec2bin(value + 2 ** i))
        time.sleep(0.001)
        if GPIO.input(comp) == 1: #0 when on DAC higher then on TROYKA(SIG)
            continue
        else:
            value += 2 ** i
    return value * 3.3 / 255

try:
    GPIO.output(dac, 0)
    curr_voltage = 0
    is_charging = True
    voltage_vals = []
    stop_voltage = 3.3 * 0.97
    delay_duration = 0.001
    time_intervals = [0]
    
    charging()
    start_time = time.time()
    
    while True:
        curr_voltage = adc_voltage()

        if curr_voltage >= stop_voltage:
            GPIO.output(troyka, 0)
            
        #time_intervals.append( time_intervals[-1] + delay_duration)
        voltage_vals.append(curr_voltage) 
        
        if curr_voltage == 0 :
            break
        
        time.sleep(delay_duration)
    
    exp_duration = time.time() - start_time
    
    with open('data.txt', 'w') as f:
        for val in voltage_vals:
                f.write(f"{val:.3f}\n")
    with open('settings.txt', 'w') as f:
        f.write(f"Discretization duration: {delay_duration}\n")
        f.write(f"Quantum step: {3.3 / 255:.4f}\n")
        f.write(f"Experiment duration: {exp_duration:.4f}\n")
    #print(vals, time_intervals)
    print(voltage_vals)
    print(time_intervals)
    plt.plot(voltage_vals)
    plt.grid()
    plt.show()
    #plt.plot(voltage_vals, time_intervals)
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
