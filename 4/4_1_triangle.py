import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

dac = [8,11,7,1,0,5,12,6]
GPIO.setup(dac, GPIO.OUT)
bnum = [0,0,0,0,0,0,0,0]


def final():
    GPIO.output(12, 0)
    p.stop()
    GPIO.cleanup()

    
p = GPIO.PWM(12, 100)
p.start(0)

def dec2bin (num):
    for i in range(0,8):
        bnum[i] = num // 2 ** (7-i)
        num = num % 2 ** (7-i)
    print(bnum)
    return bnum
    

def tryy():
        period = float(input('Enter period(sec): '))        
        steptime = period / 200
        
        while True:
            for ampl in range(256):
                number = dec2bin(ampl)
                GPIO.output(dac, number)
                time.sleep(steptime)
            for ampl in range(255, -1, -1):
                GPIO.output(dac, dec2bin(ampl))
                time.sleep(steptime)


tryy()
final()
