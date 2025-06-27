import torch
import cv2
import easyocr
import numpy as np
import os
from pathlib import Path

YOLOMODEL = torch.hub.load('yolov5', 'yolov5s',pretrained = True)
reader = easyocr.Reader(['en'], gpu=False)

PLATECLASSES = ['licence plate', 'car', 'truck', 'bus']

def detectPlate(frame):
    result = YOLOMODEL(frame)
    for det in result.xyxy[0]:
        xmin, ymin, xmax, ymax, conf, cls = det
        className = YOLOMODEL.names[int(cls)]
        
        if className in PLATECLASSES:
            xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
            cropped = frame[ymin:ymax, xmin:xmax]
            
            results = reader.readtext(cropped)
            if result:
                text = result[0][1]
                print(f"[INFO] Detected plate: {text}")
                return text, cropped
            
    return None, None