
import datetime
import constants
import database

next_event_id = str

def begin():

    # Convert the current date to day-of-the-year.
    # If it is later than the last event, set it to the date of the first event.

    global next_event_id

    date_format = '%a %b %d'
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()

    first_datetime = datetime.datetime.strptime(constants.event_ids[0], date_format)
    first_date = datetime.date(current_date.year, first_datetime.month, first_datetime.day)

    last_datetime = datetime.datetime.strptime(constants.event_ids[-1], date_format)
    last_date = datetime.date(current_date.year, last_datetime.month, last_datetime.day)

    if current_date > last_date: # You must be working on next year's calendar.
        current_date = first_date

    for event_id in constants.event_ids:

        next_event_datetime = datetime.datetime.strptime(event_id, date_format)
        next_event_date = datetime.date(current_date.year, next_event_datetime.month, next_event_datetime.day)

        if next_event_date < current_date: pass
        else:
            next_event_id = event_id
            break

    return

def add_info(event):

    # Store details of the participants in the next event.

    global next_event_id

    if event["date"] == next_event_id:
        for crew in event["flotilla"]:
            boat_name = [boat["display name"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
            database.crew_info += boat_name + " "
            boat_mobile = [boat["mobile"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
            database.crew_info += boat_mobile + "\n\n"
            for event_sailor in crew["sailors"]:
                for sailor in database.sailors_data:
                    if event_sailor == sailor["key"]:
                        database.crew_info += sailor["display name"] + "\n"
                        experience = sailor["experience"]
                        experience = experience.replace("+u002C", ",")
                        experience = experience.replace("+u2028", "\n")
                        experience.rstrip("\n") # Replace one or more "\n" characters with two "\n" characters.
                        database.crew_info += experience + "\n" + "\n"
            database.crew_info += "\n"
    return
