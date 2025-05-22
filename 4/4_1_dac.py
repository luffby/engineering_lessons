import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


leds = [2,3,4,17,27,22,10,9]
dac = [8,11,7,1,0,5,12,6]
bnum = [0,0,0,0,0,0,0,0]

WasAnErr = False

GPIO.setup(dac, GPIO.OUT)


def final():
    GPIO.output(dac, 0)
    GPIO.cleanup()
    
def tryy():
    while True:
        print('Enter an integer between 0 and 255')
        pos = 1
        num = 0
        num_str = input()
        
        for i in range(0,len(num_str)):
            if num_str[i] > '0' and num_str[i] < '9':
                num = num * 10 + int(num_str[i])
                pos = pos + 1
            else:
                print('Err: not an integer, wrong character at pos ', pos)
                WasAnErr = True
                break
        
        if WasAnErr:
            continue
        print(num)
        
    
    for i in range(0,8):
        bnum[i] = num // 2 ** (7-i)
        num = num % 2 ** (7-i)
    GPIO.output(dac, bnum)

GPIO.output(dac, 0)
tryy()
print(bnum)
time.sleep(5)
final()
