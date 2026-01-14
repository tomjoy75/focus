#!/usr/bin/env python3
import  sys
import  os
from    pathlib import Path
import  datetime

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
    data_dir = get_data_dir()
    time = datetime.datetime.now()
    filename = time.strftime("%Y-%m-%d.json")
    print(f"Using data directory : {data_dir}")
    print(f"Name of the file     : {filename}")
    with open(data_dir + "/" + filename) as f:


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
