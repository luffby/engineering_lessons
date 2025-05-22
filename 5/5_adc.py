import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in format (value, '08b')]

def adc():#1TASK
    for value in range(256):
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.01)
        if GPIO.input(comp) == 1: #0 when on DAC higher then on TROYKA(SIG)
              return value
    return 255

def adc1():#2TASK
    value = 0
    for i in range(7,-1, -1):
        GPIO.output(dac, dec2bin(value + 2 ** i))
        time.sleep(0.001)
        if GPIO.input(comp) == 1: #1 - no
            continue
        else:
            value += 2 ** i
    return value

def mk_led(led_num): #3TASK
    ans = [0,0,0,0,0,0,0,0]
    for i in range(0, led_num):
        ans[i] = 1
    for i in range(led_num, 8):
        ans[i] = 0
    return ans

def led_on(val): #3TASK
    led_num = int(round((val / 256 * 8), 1))
    print("led num: ", led_num)
    GPIO.output(leds, mk_led(led_num))

try:
    while True:
        value = adc1()
        v = value * 3.3 / 255
        print(f"adc: {value}, voltage: {v}")
        led_on(value)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
