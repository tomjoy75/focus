#!/usr/bin/env python3
import  sys

def cmd_start():
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
