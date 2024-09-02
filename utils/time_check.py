from datetime import datetime
import pytz

def print_current_time():
    tz = pytz.timezone('Asia/Kolkata')  # or your preferred timezone
    now = datetime.now(tz)
    print(f"Current server time: {now}")

if __name__ == "__main__":
    print_current_time()
