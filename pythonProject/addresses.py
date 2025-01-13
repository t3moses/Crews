
import database

def begin():

    database.addresses = ""

    return

def add_date( event_date ):

    database.addresses += event_date + "\n\n"

    return

def add_boats( event ):

    addresses = ""

    database.addresses += "boats\n\n"

    index = 0
    for crew in event["flotilla"]:
        for boat in database.boats_data:
            if crew["boat"] == boat["key"]:
                if not index == 0:
                    addresses += ", "
                index += 1
                addresses += boat["email address"]

    database.addresses += addresses + "\n\n"

    return

def add_sailors( event ):

    addresses = ""

    database.addresses += "sailors\n\n"

    index = 0
    for crew in event["flotilla"]:
        for event_sailor in crew["sailors"]:
            for sailor in database.sailors_data:
                if event_sailor == sailor["key"]:
                    if not index == 0:
                        addresses += ", "
                    index += 1
                    addresses += sailor["email address"]

    database.addresses += addresses + "\n\n"

    return
