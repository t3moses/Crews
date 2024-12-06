
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

def add_info(flotilla, event_date):

    # Store details of the next event.

    global next_event_date

    if event_date == next_event_date:
        for crew in flotilla["crews"]:
            database.crew_info += crew["boat"]["display name"] + "\n"
            for sailor in crew["sailors"]:
                database.crew_info += " " + sailor["display name"] + "\n"
                for database_sailor in database.sailors_data:
                    if database_sailor["key"] == sailor["key"]:
                        experience = database_sailor["experience"]
                        experience = experience.replace("&#44;", ",")
                        experience = experience.replace("&#10;", ",\n")
                database.crew_info += experience + "\n"
    return
