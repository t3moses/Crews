
import database

def begin():

    database.addresses = ""

    return

def add_date( event_date ):

    database.addresses += event_date + "\n\n"

    return

def add_boats( flotilla ):

    addresses = ""

    database.addresses += "boats\n\n"

    index = 0
    for crew in flotilla["crews"]:
        for boat in database.boats_data:
            if crew["boat"]["key"] == boat["key"]:
                if not index == 0:
                    addresses += ", "
                index += 1
                addresses += boat["email address"]

    database.addresses += addresses + "\n\n"

    return

def add_sailors( flotilla ):

    addresses = ""

    database.addresses += "sailors\n\n"

    index = 0
    for crew in flotilla["crews"]:
        for flotilla_sailor in crew["sailors"]:
            for sailor in database.sailors_data:
                if sailor["key"] == flotilla_sailor["key"]:
                    if not index == 0:
                        addresses += ", "
                    index += 1
                    addresses += sailor["email address"]

    database.addresses += addresses + "\n\n"

    return
