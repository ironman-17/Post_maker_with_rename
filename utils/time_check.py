from datetime import datetime
import pytz

# Define your timezone
tz = pytz.timezone('Asia/Kolkata')  # Replace with your timezone

# Get current time
now = datetime.now(tz)
print(f"Current time: {now}")
