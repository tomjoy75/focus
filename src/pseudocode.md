function get_data_dir()
// Recupere le path du json a partir de la variable d'environnement FOCUS_DATA_DIR
    read environment variable FOCUS_DATA_DIR
    
    if not defined:
        print error and exit

    if path does not exist:
        print error and exit

    if path is not a directory:
        print error and exit

    return path


fonction cmd_start()
// Recupere le json stocke dans un fichier de type YYYY-MM-DD.json
// Checke le fichier 
// Affiche le prompt "🎯 What are you going to do now?"
// Enregistre la reponse de l'utilisateur, ainsi que l'horodatage dans le .json

    data_dir = get_data_dir()
    today = current date as "YYYY-MM-DD"
    filename = today + ".json"
    path = join(data_dir, filename)

    if file exists at path:
        try:
            open file
            read text
            parse JSON into data
        except parsing error:
            print "Invalid session file format"
            exit

    else:
        data = {
            "date": today,
            "sessions": []
        }

    sessions = data["sessions"]

    if sessions is not empty:
        last_session = sessions[-1]
        if "end" not in last_session:
            print "⚠️ A focus session is already running."
            print "Use `focus status` to check it."
            exit

    print "🎯 What are you going to do now?"
    intent = read user input (blocking)

    start_time = current time as "HH:MM"

    new_session = {
        "intent": intent,
        "start": start_time,
        "planned_min_duration": 25
    }

    append new_session to data["sessions"]

    write data as JSON to path (create or overwrite file)

    exit silently


fonction cmd_status()
// Recupere le fichier date d'aujourd'hui
//1/ Charger statut du jour
//2/ Trouver la derniere session
//3/ elapsed = now - start
//4/ < duration_per_session -> "Not Yet. Stay focused"
     >= duration_per_session -> "You can take a break"
                                "Press enter to end the session"