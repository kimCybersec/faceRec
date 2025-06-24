import cv2
import numpy as np
from mtcnn import MTCNN
from sklearn.preprocessing import Normalizer
from facenetUtils import loadFacenetModel, getEmbedding, loadKnownFaces, matches

def recogniseFaces(modelPath='models/facenet_keras.h5', facesDir='media/faces'):
    print("[*]Loadning facenet model and known faces.....")
    model = loadFacenetModel(modelPath)
    knownFaces = loadKnownFaces(model, facesDir)
    normalizer = Normalizer('12')
    
    detector = MTCNN()
    cap = cv2.VideoCapture(0)
    
    print("[*]Starting camera.......")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        faces = detector.detect_faces(frame)
        for face in faces:
            x, y, width, height = face['box']
            x, y = abs(x), abs(y)
            faceImg = frame[y:y+height, x:x+width]
            try:
                embedding = getEmbedding(model, faceImg)
                embedding = normalizer.transform([embedding])[0]
                identity = "unknown"
                bestScore = 0.0
                
                for name, knownEmbedding in knownFaces.items():
                    match, score = matches(knownEmbedding, embedding)
                    if match and score > bestScore:
                        identity = name
                        bestScore = score
                        
                cv2.rectangle(frame, (x,y), (x+width, y+height), (0, 255, 0) if identity != "Unknown" else (255, 0, 0), 2)
                cv2.