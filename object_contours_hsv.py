import time
import numpy as np
import cv2
from picamera2 import Picamera2

picam = Picamera2()
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
picam.preview_configuration.main.size = (FRAME_WIDTH, FRAME_HEIGHT)
picam.preview_configuration.main.format = 'RGB888'
picam.preview_configuration.controls.FrameRate = 60
picam.preview_configuration.align()
picam.configure('preview')
picam.start()

out = cv2.VideoWriter('test3.avi', cv2.VideoWriter_fourcc(*'XVID'), 60.0, (1280, 720))
out2 = cv2.VideoWriter('test4.avi', cv2.VideoWriter_fourcc(*'XVID'), 60.0, (640, 360))

fps = 0
hue_low, hue_high = 0, 0
sat_low, sat_high = 0, 0
val_low, val_high = 0, 0

def track_hue_low(val):
    global hue_low
    hue_low = val
    print(f'hue low: {hue_low}')
    
def track_hue_high(val):
    global hue_high
    hue_high = val
    print(f'hue high: {hue_high}')
    
def track_sat_low(val):
    global sat_low
    sat_low = val
    print(f'sat low: {sat_low}')
    
def track_sat_high(val):
    global sat_high
    sat_high = val
    print(f'sat high: {sat_high}')
    
def track_val_low(val):
    global val_low
    val_low = val
    print(f'val low: {val_low}')
    
def track_val_high(val):
    global val_high
    val_high = val
    print(f'val high: {val_high}')
    

cv2.namedWindow('Trackbars')
cv2.createTrackbar('Hue Low', 'Trackbars', 0, 179, track_hue_low)
cv2.createTrackbar('Hue High', 'Trackbars', 0, 179, track_hue_high)
cv2.createTrackbar('Sat Low', 'Trackbars', 0, 255, track_sat_low)
cv2.createTrackbar('Sat High', 'Trackbars', 0, 255, track_sat_high)
cv2.createTrackbar('Val Low', 'Trackbars', 0, 255, track_val_low)
cv2.createTrackbar('Val High', 'Trackbars', 0, 255, track_val_high)


while True:
    t0 = time.time()
    frame = picam.capture_array()
    cv2.putText(frame, str(int(fps)), (1100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (244, 240, 250), 1)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, np.array([hue_low, sat_low, val_low]), np.array([hue_high, sat_high, val_high]))
    ooi = cv2.bitwise_and(frame, frame, mask=mask)
    ooi_small = cv2.resize(ooi, (FRAME_WIDTH//2, FRAME_HEIGHT//2))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        contour = contours[0]
        # cv2.drawContours(frame, contours, 0, (255,0,0), 3)
        x, y, w, h  = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 240, 240),3)
    
    cv2.imshow('picam', frame)
    cv2.imshow('ooi', ooi_small)
    out.write(frame)
    out2.write(ooi_small)
    if cv2.waitKey(1) == ord('q'):
        break
    fps = 0.9*fps + 0.1*(1//(time.time() - t0))

out.release()
out2.release()
cv2.destroyAllWindows()