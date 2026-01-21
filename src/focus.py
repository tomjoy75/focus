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
        sys.exit()

    path = Path(data_dir).expanduser()

    if not path.exists() or not path.is_dir():
        print(f"⚠️ FOCUS_DATA_DIR points to an invalid directory:")
        print(f"  {path}")
        sys.exit(1)
    return path

def cmd_start():
    # Se refaire un schema en pseudo code a avoir sous la main
    # Diviser la fonction pour ne pas etre trop machine a gaz
    data_dir = get_data_dir()
    time = datetime.datetime.now()
    filename = time.strftime("%Y-%m-%d.json")
    path = data_dir / filename

    print(f"Using data directory : {data_dir}")
    print(f"Name of the file     : {filename}")
    print(f"Path of the file     : {path}")

    if path.is_file():
        print(f"{path} exists")
        with open(path, "r"):
            data = json.loads(f.read())
    else :
        print(f"{path} do not exist")
        data = {
            "date": time.strftime("%Y-%m-%d"),
            "sessions": []
        }
        print("Initialized empty daily state")

    sessions = data["sessions"]
    if len(sessions) != 0:
        last = sessions[-1]
        if "end" not in last:
            print("⚠️ A focus session is already running.")
            print("Use `focus status` to check it.")
            sys.exit()

    print("Starting focus session WIP")

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
