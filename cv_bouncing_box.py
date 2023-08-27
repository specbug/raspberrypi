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
fps = 0

rect_ul = [50, 20]
rect_br = [150, 120]
rect_color = (0,0,255)
rect_thickness = -1
dr, dc = 5, 5


while True:
    t0 = time.time()
    frame = picam.capture_array()
    cv2.putText(frame, str(int(fps)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (244, 240, 250), 1)
    rect_ul[0] += dc
    rect_ul[1] += dr
    rect_br[0] += dc
    rect_br[1] += dr
    
    if rect_ul[0] <= 0 or rect_br[0] >= FRAME_WIDTH:
        dc *= -1
    if rect_ul[1] <= 0 or rect_br[1] >= FRAME_HEIGHT:
        dr *= -1
    
    cv2.rectangle(frame, rect_ul, rect_br, rect_color, rect_thickness)
    cv2.imshow('picam', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    fps = 0.9*fps + 0.1*(1//(time.time() - t0))

cv2.destroyAllWindows()