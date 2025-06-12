import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate 
import json
import os


LOG_FILE = "coding_log.json"


if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as file:
        coding_log = json.load(file)
else:
    coding_log = []


def add_to_log(start_time, end_time, duration_minutes):
    entry = {
        "Date": start_time.strftime("%Y-%m-%d"),
        "Start Time": start_time.strftime("%H:%M:%S"),
        "End Time": end_time.strftime("%H:%M:%S"),
        "Duration (mins)": round(duration_minutes)
    }
    coding_log.append(entry)

    with open(LOG_FILE, "w") as file:
        json.dump(coding_log, file, indent=4)
        

def show_log_table():
    if not coding_log:
        print("\n📭 No coding sessions logged yet.")
    else:
        print("\n🧾 Coding Log:")
        print(tabulate(coding_log, headers="keys", tablefmt="grid"))
        

def countdown_timer():
    try:
        print("\nEnter the time for the countdown:")
        hours = int(input("Hours: ") or 0)
        minutes = int(input("Minutes: ") or 0)
        seconds = int(input("Seconds: ") or 0)

        if hours < 0 or minutes < 0 or seconds < 0:
            print("❌ Time values must not be negative.")
            return

        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds == 0:
            print("\n❌ Please enter a time greater than 0.")
            return

        start_time = datetime.now()
        print(f"\n✅ Timer started at {start_time.strftime('%H:%M:%S')}")

        while total_seconds > 0:
            hrs, rem = divmod(total_seconds, 3600)
            mins, secs = divmod(rem, 60)
            print(f"⏱️ {hrs:02d}:{mins:02d}:{secs:02d}", end='\r')
            time.sleep(1)
            total_seconds -= 1

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() / 60
        
        add_to_log(start_time, end_time, duration)

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("⏰ Timer Done", f"You coded for {round(duration)} minutes!. Time to take a break and eat!")
        print()

    except ValueError:
        print("\n❌ Invalid input. Please enter whole numbers.")
        
        
def delete_log_entry():
    if not coding_log:
        print("\n📭 No records to delete.")
        return

    while True:
        print("\n🧾 Current Log:")
        for idx, entry in enumerate(coding_log):
            print(f"{idx + 1}. {entry}")

        try:
            choice = input("\nEnter record number to delete (or press Enter to stop): ")
            if choice.strip() == "":
                break

            index_to_delete = int(choice) - 1

            if 0 <= index_to_delete < len(coding_log):
                deleted = coding_log.pop(index_to_delete)
                print(f"\n✅ Deleted: {deleted}")

                with open(LOG_FILE, "w") as file:
                    json.dump(coding_log, file, indent=4)
            else:
                print("\n❌ Invalid record number.")
        except ValueError:
            print("\n❌ Please enter a valid number.")
            

while True:
    print("\nMENU:")
    print("1. Start a new coding timer")
    print("2. View coding log")
    print("3. Delete a log entry")
    print("0. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        countdown_timer()
    elif choice == '2':
        show_log_table()
    elif choice == '3':
        delete_log_entry()
    elif choice == '0':
        print("👋 Goodbye!")
        break
    else:
        print("\n❌ Invalid choice. Try again.")

