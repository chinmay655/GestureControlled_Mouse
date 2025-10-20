import time
import cv2

def draw_fps(frame, p_time):
    c_time = time.time()
    fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    return c_time
