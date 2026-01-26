#!/usr/bin/env python3
import  sys
import  os
from    pathlib import Path
import  datetime
import  json

def get_data_dir():
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

def init_data(path, today_str) -> {} :
    if path.is_file():
        with open(path, "r") as f:
            try :
                data = json.loads(f.read())
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) :
                print(f"⚠️ Invalid session file format.\nPlease fix or delete the file:\t{path}")
                return
    else :
        data = {
            "date": today_str,
            "sessions": []
        }
        print("Initialized empty daily state")
    return data
    

def cmd_start():
    # Se refaire un schema en pseudo code a avoir sous la main
    # Diviser la fonction pour ne pas etre trop machine a gaz
    data_dir = get_data_dir()
    time = datetime.datetime.now()
    today_str = time.strftime("%Y-%m-%d")
    filename = time.strftime(f"{today_str}.json")
    path = data_dir / filename 
    print(f"Path of the file     : {path}")

    data = init_data(path, today_str)

    sessions = data["sessions"]
    if not isinstance(sessions, list):
        print("⚠️ Invalid session file format.")
        return 1
    if len(sessions) != 0:
        last = sessions[-1]
        if "end" not in last:
            print("⚠️ A focus session is already running.")
            print("Use `focus status` to check it.")
            return(1)

    while True:
        print("🎯 What are you going to do now?")
        intent = input()
        if intent.strip() != "":
            break
        else:
            print("Your answer is empty, please enter a valid answer.")

    time = datetime.datetime.now()
    start_time = time.strftime("%H:%M")
    new_session = {
        "intent" : intent,
        "start" : start_time,
        "planned_min_duration" : 25
    }
    sessions.append(new_session)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    return 0




def cmd_status():
    print("Checking focus session WIP")

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
            cmd_start()
        case "status":
            cmd_status()
        case "help" | "-h" :
            cmd_help()
        case _ :
            print(f"unknown command : {cmd}")
            cmd_help()

    #print("focus CLI - work in progress")

if __name__=="__main__":
    main()
