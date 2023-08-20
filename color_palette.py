import time
import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    ra = GPIO.PWM(40, 100)
    ga = GPIO.PWM(38, 100)
    ba = GPIO.PWM(36, 100)
    
    rp = gp = bp = 1
    step = 5
    rdc = gdc = bdc = 0
    
    ra.start(0)
    ga.start(0)
    ba.start(0)
    
    while True:
        r = GPIO.input(37)
        g = GPIO.input(35)
        b = GPIO.input(31)
        
        if r and not rp:
            rdc = (rdc + step)%100
        if g and not gp:
            gdc = (gdc + step)%100
        if b and not bp:
            bdc = (bdc + step)%100
        
        ra.ChangeDutyCycle(rdc)
        ga.ChangeDutyCycle(gdc)
        ba.ChangeDutyCycle(bdc)
        
        rp, gp, bp = r, g, b
        time.sleep(0.1)
        
except Exception as exc:
    print(exc)
finally:
    GPIO.cleanup()
