import os
import time
from datetime import datetime
import pytz

def sync_time():
    tz = pytz.timezone('Asia/Kolkata')  
    now = datetime.now(tz)
    print(f"Syncing server time: {now}")
    
if __name__ == "__main__":
    sync_time()
    time.sleep(60)  
