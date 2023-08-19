import time
import RPi.GPIO as GPIO

led_pin_map = [11, 13, 15, 16, 18]
led_state_map = [0]*5

try:
    GPIO.setmode(GPIO.BOARD)
    for pin in led_pin_map:
        GPIO.setup(pin, GPIO.OUT)

    for i in range(1, 32):
        for p in range(5):
            b = i >> p & 1
            led_state_map[p] = b
        for p in range(5):
            GPIO.output(led_pin_map[p], led_state_map[p])
        time.sleep(1)
except Exception as exc:
    print(exc)
finally:
    GPIO.cleanup()
