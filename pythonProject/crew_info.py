
import datetime
import constants
import database

next_event_date = str

def begin():

    # Convert the current date to day-of-the-year.
    # If it is later than the last event, set it to the date of the first event.

    global next_event_date

    database.crew_info = ""
    date_format = '%a %b %d'

    current_datetime = datetime.datetime.now()
    first_day = datetime.datetime.strptime(constants.event_dates[0], date_format)
    last_datetime = datetime.datetime.strptime(constants.event_dates[-1], date_format)
    if current_datetime > last_datetime:
        current_day = int(first_day.timetuple().tm_yday)

    for event_date in constants.event_dates:
        event_day = datetime.datetime.strptime(event_date, date_format).timetuple().tm_yday
        if event_day > current_day:
            return
        else:
            next_event_date = event_date

    return

def add_info(event):

    # Store details of the participants in the next event.

    global next_event_date

    if event["date"] == next_event_date:
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
                        experience.rstrip("\n")
                        experience += "\n"
                        database.crew_info += experience + "\n"
            database.crew_info += "\n"
    return
