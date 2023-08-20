import time
import RPi.GPIO as GPIO

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pwm = GPIO.PWM(40, 120)
    step = 99//9
    duty_cycle = 0

    b1_state = b2_state = 1
    out = False
    pwm.start(0)

    while True:
        ip1 = GPIO.input(37)
        ip2 = GPIO.input(35)
        if ip1 and not b1_state:
            out = True
            duty_cycle += step
        if ip2 and not b2_state:
            out = False
            duty_cycle -= step
        duty_cycle = min(100, max(0, duty_cycle))
        pwm.ChangeDutyCycle(duty_cycle)
        b1_state = ip1
        b2_state = ip2
        time.sleep(0.1)
except Exception as exc:
    print(exc)
finally:
    pwm.stop()
    GPIO.cleanup()