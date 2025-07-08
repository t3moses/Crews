
import datetime
import constants
import database

def add_info(event):

    # Store details of the participants in the next event.

    for crew in event["flotilla"]:
        boat_name = [boat["display name"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
        database.crew_info += boat_name + " "
        boat_mobile = [boat["mobile"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
        database.crew_info += boat_mobile + "\n\n"
        for event_sailor in crew["sailors"]:
            for sailor in database.sailors_data:
                if event_sailor == sailor["key"]:
                    database.crew_info += sailor["display name"] + "\n"
                    database.crew_info += sailor["email address"] + "\n"
                    experience = sailor["experience"]
                    experience = experience.replace("+u002C", ",")
                    experience = experience.replace("+u2028", "\n")
                    experience.rstrip("\n") # Replace one or more "\n" characters with two "\n" characters.
                    database.crew_info += experience + "\n" + "\n"
        database.crew_info += "\n"
    return
