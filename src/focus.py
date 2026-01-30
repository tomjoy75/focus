#!/usr/bin/env python3
import  sys
import  os
from    pathlib import Path
from  datetime import datetime
import  json

def get_data_dir():
    """
    Return the directory used to store focus session data.

    - The dir path is read from the FOCUS_DATA_DIR environment variable.
    - Raises an exception if the variable is missing or invalid
    """

    data_dir = os.getenv("FOCUS_DATA_DIR")

    if not data_dir:
        raise Exception(
            "⚠️ FOCUS_DATA_DIR is not set.\n"
            "Example:\n"
            "  export FOCUS_DATA_DIR=~/GoogleDrive/focus")
    path = Path(data_dir).expanduser()
    if not path.exists() or not path.is_dir():
        raise Exception(
            "⚠️ FOCUS_DATA_DIR points to an invalid directory:\n"
            f"  {path}")
    return path

def init_data(path, today_str) -> dict :
    """
    Return a json used to store all the elements of today's session  

    - Open the json from today's file, or create a new one 
    - Raises an exception if the json is not correctly extracted 
    """
    
    if path.is_file():
        with open(path, "r") as f:
            try :
                data = json.loads(f.read())
            except (ValueError, json.JSONDecodeError, UnicodeDecodeError) :
                raise Exception(f"⚠️ Invalid session file format.\nPlease fix or delete the file:\t{path}")
    else :
        data = {
            "date": today_str,
            "sessions": []
        }
        print("Initialized empty daily state")
    return data
    
def check_data(data) -> list :
    """
    Validate session data for a new start.

    - Ensures the sessions list is valid and no session is already running.
    - Raises an exception if the format is invalid or a session is active
    """

    sessions = data["sessions"]
    if not isinstance(sessions, list):
        raise Exception("⚠️ Invalid session file format.")
    if len(sessions) != 0:
        last = sessions[-1]
        if "end" not in last:
            raise Exception(
                "⚠️ A focus session is already running.\n"
                "Use `focus status` to check it.")
    return sessions

def prompt_user() -> str:
    """
    Ask the user for his intent for the next session.

    - Repeats the prompt until a non-empty string is provided.
    """
    
    while True:
        print("🎯 What are you going to do now?")
        intent = input()
        if intent.strip() != "":
            break
        else:
            print("Your answer is empty, please enter a valid answer.")
    return intent


def start_session(intent, duration, path, data):
    """
    Create and store a new focus session.

    - Appends a session to the in-memory data and writes the JSON file.
    """

    time = datetime.now()
    start_time = time.isoformat()
    new_session = {
        "intent" : intent,
        "start" : start_time,
        "planned_min_duration" : duration
    }
    data["sessions"].append(new_session)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

def cmd_start():
    """
    Start a new focus session from the CLI.

    - Loads or initializes today's data, then prompts and writes a session.
    """

    try:
        data_dir = get_data_dir()
        time = datetime.now()
        today_str = time.strftime("%Y-%m-%d")
        filename = time.strftime(f"{today_str}.json")
        path = data_dir / filename 
        print(f"Path of the file     : {path}")
        data = init_data(path, today_str)
        sessions = check_data(data)
    except Exception as e:
        print(e)
        return 1
    intent = prompt_user()
    start_session(intent, 25, path, data)

    return 0

def cmd_status():
    """
    Check the status of today's focus session.

    - Reads today's file and reports whether a session is currently running.
    - Checks also if the session duration his completed
    - In case it's completed, it record an end key in the session dictionnary
    - Raises an exception if
    """

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
    """
    Print the CLI help message.

    Lists available commands and their usage.
    Does not raise any exception
    """
    
    print("focus start  -> start a session")
    print("focus status -> check if you can pause")
    print("focus help   -> show this help")

def main():
    """
    Dispatch the CLI command.

    Parses arguments and routes to the appropriate command handler.
    """

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

if __name__=="__main__":
    main()
