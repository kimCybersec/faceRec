import json
from datetime import datetime
import os

def logPlateEntry(plateNumber, logPath = "database/plateLogs.json"):
    os.makedirs(os.path.dirname(logPath), exist_ok=True)
    logEntry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plateNumber": plateNumber
    }
    
    if not os.path.exists(logPath):
        with open(logPath, 'w') as f:
            json.dump([logEntry], f, indent=4)
            
    else:
        with open(logPath, 'r+') as f:
            data = json.load(f)
            data.append(logEntry)
            f.seek(0)
            json.dump(data, f, indent=4)
            
    print(f"[*] Logged vehicle {plateNumber}")
    