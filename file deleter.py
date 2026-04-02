import os
import time
from send2trash import send2trash
from datetime import datetime, timedelta

def clean_old_files(target_folder, exceptions):
    #Calculae the cutoff date (approx. 182 days)
    six_months_ago = datetime.now() - timedelta(days=182)
    cutoff_seconds = six_months_ago.timestamp()

    print(f"Checking for files older than: {six_months_ago.strftime('%Y-%m-%d')}")

    for root, dirs, files in os.walk(target_folder):
        for name in files:
            file_path = os.path.join(root, name)

            #1. Check Exceptions
            if any(exc.lower() in name.lower() for exc in exceptions):
                continue

            # 2. Check Age
            try:
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_seconds:
                    print(f"Moving to Recycle Bin: {name}")
                    send2trash(file_path)
            except Exception as e:
                print(f"Error processing {name}: {e}")

# ---- User Interaction ----
folder_to_clean = input("Enter the full path of the folder to monitor: ")
user_exceptions = input("Enter keywords/filenames to ignore (separated by commas): ").split(',')
# Clear whitespace from user input
user_exceptions = [item.strip() for item in user_exceptions if item.strip()]

if os.path.exists(folder_to_clean):
    clean_old_files(folder_to_clean, user_exceptions)
else:
    print("Invalid folder path.")