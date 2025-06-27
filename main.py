from database.models import initDb
from database.dbUtils import imgEntry
import cv2
from plateModule.plateOcr import detectPlate

def plateRecognition():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        text, croppedPlate = detectPlate(frame)
        if text:
            imgEntry(identity=text, entryType="plate")
            cv2.putText(frame, f"Plate: {text}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            
        cv2.imshow("YOLO Plate Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    plateRecognition()
    initDb()