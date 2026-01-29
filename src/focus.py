#!/usr/bin/env python3
import  sys
import  os
from    pathlib import Path
from  datetime import datetime
# from    datetime import date
import  json

def get_data_dir():
    # Use env_variable FOCUs_DATA_DIR to get the path
    data_dir = os.getenv("FOCUS_DATA_DIR")

    if not data_dir:
        print("⚠️ FOCUS_DATA_DIR is not set.")
        print("Example:")
        print("  export FOCUS_DATA_DIR=~/GoogleDrive/focus")
        return 1
    path = Path(data_dir).expanduser()
    if not path.exists() or not path.is_dir():
        print(f"⚠️ FOCUS_DATA_DIR points to an invalid directory:")
        print(f"  {path}")
        return 1
    return path

def init_data(path, today_str) -> dict | None :
    # Initialise data
    if path.is_file():
        with open(path, "r") as f:
            try :
                data = json.loads(f.read())
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) :
                print(f"⚠️ Invalid session file format.\nPlease fix or delete the file:\t{path}")
                return None
    else :
        data = {
            "date": today_str,
            "sessions": []
        }
        print("Initialized empty daily state")
    return data
    
def check_data(data) -> list | None:
    # Check if data is a list and end is present
    sessions = data["sessions"]
    if not isinstance(sessions, list):
        print("⚠️ Invalid session file format.")
        return None
    if len(sessions) != 0:
        last = sessions[-1]
        if "end" not in last:
            print("⚠️ A focus session is already running.")
            print("Use `focus status` to check it.")
            return None
    return sessions

def prompt_user() -> str:
    while True:
        print("🎯 What are you going to do now?")
        intent = input()
        if intent.strip() != "":
            break
        else:
            print("Your answer is empty, please enter a valid answer.")
    return intent


def start_session(intent, duration, path, data):
    time = datetime.now()
    start_time = time.isoformat()
    # start_time = time.strftime("%H:%M")
    new_session = {
        "intent" : intent,
        "start" : start_time,
        "planned_min_duration" : duration
    }
    data["sessions"].append(new_session)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

def cmd_start():
    # Start a new session
    data_dir = get_data_dir()
    time = datetime.now()
    today_str = time.strftime("%Y-%m-%d")
    filename = time.strftime(f"{today_str}.json")
    path = data_dir / filename 
    print(f"Path of the file     : {path}")

    data = init_data(path, today_str)
    if data is None:
        return 1

    sessions = check_data(data)
    if sessions is None:
        return 1

    intent = prompt_user()
    if intent is None:
        return 1

    start_session(intent, 25, path, data)

    return 0

def cmd_status():
    print("Checking focus session WIP")
    data_dir = get_data_dir()
    time = datetime.now()
    filename = time.strftime("%Y-%m-%d.json")
    path = data_dir / filename
    print(f"DEBUG: path : {path}")
    if path.is_file():
        with open(path, "r") as f:
            try :
                data = json.loads(f.read())
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) :
                print(f"⚠️ Invalid session file format.\nPlease fix or delete the file:\t{path}")
                return 1
    else :
        print("⚠️ No focus session is opened for today.")
        print("Use `focus start` to start one.")
        return 1
    sessions = data["sessions"]
    print(f"DEBUG: sessions : {sessions}")
    if len(sessions) == 0:
        print("⚠️ No session for today is already started.")
        print("Use `focus start` to start one.")
        return 1
    last = sessions[-1]
    if "end" in last:
        print("⚠️ Last focus session is already finished.")
        print("Use `focus start` to start a new one.")
        return 1
    time = datetime.now()
    start_time = datetime.fromisoformat(last["start"])
    print(f"actual time : {time}, start time : {start_time}")
    print(f"actual time : {time}, start time : {start_time}, duration : {time - start_time}")
    

    return 0

    


def cmd_help():
    print("focus start  -> start a session")
    print("focus status -> check if you can pause")
    print("focus help   -> show this help")

def main():
    if len(sys.argv) < 2 :
        cmd_help()
        return

    cmd = sys.argv[1]
    match(cmd):
        case "start":
            return cmd_start()
        case "status":
            return cmd_status()
        case "help" | "-h" :
            cmd_help()
            return 0
        case _ :
            print(f"unknown command : {cmd}")
            cmd_help()
            return 1

    #print("focus CLI - work in progress")

if __name__=="__main__":
    main()
