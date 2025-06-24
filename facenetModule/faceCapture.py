import cv2
import os
from mtcnn import MTCNN

def captureFaces(username: str, saveDir = "media/faces", numSamples=10):
    detector = MTCNN()
    cap = cv2.VideoCapture(0)
    
    userPath = os.path.join(saveDir, username)
    count = 0
    
    while count < numSamples:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        
        faces = detector.detect_faces(frame)
        if faces:
            x, y, width, height = faces[0]['box']
            face = frame[y:y+height, x:x+width]
            face = cv2.resize(face, (160, 160))
            
            facePath = os.path.join(userPath, f"{count}.jpg")
            cv2.imwrite(facePath, face)
            print(f"[+] Saved: {facePath}")
            count+=1
            
        cv2.imshow("Capturing Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()