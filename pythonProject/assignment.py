
import copy
import database
import addresses
import crew_info
import random
import datetime
import constants
import mandatory
import discretionary
import crew_html

def assignment():

    # This function assigns sailors to boats using the mandatory and discretionary policies.

    date_format = '%a %b %d'
    current_datetime = datetime.datetime.now()
    first_date = datetime.datetime.strptime(constants.event_dates[0], date_format)
    last_date = datetime.datetime.strptime(constants.event_dates[-1], date_format)
    if current_datetime > last_date:
        current_datetime = first_date

    addresses.begin()
    crew_info.begin()

    random.seed(None)

    for event_date in constants.event_dates:

        record = {}
        record["date"] = event_date
        database.debug.append(record)

        addresses.add_date(event_date)

        event_datetime = datetime.datetime.strptime(event_date, date_format)

        random.seed(event_date)

        if current_datetime <= event_datetime:

            for sailor in database.sailor_histories:
                sailor[event_date] = ""

            # List the boats and sailors available on the event date.

            available_boat_keys = []  # list of boats available on the event date.
            for available_boat in database.boats_availability:
                if not available_boat[event_date] == "":
                    available_boat_keys.append(available_boat["key"])

            available_sailor_keys = []  # list of sailors available on the event date.
            for available_sailor in database.sailors_availability:
                if not available_sailor[event_date] == '':
                    for sailor in database.sailors_data:
                        if available_sailor["key"] == sailor["key"]:
                            available_sailor_keys.append(sailor["key"])

            # For each available boat and sailor, calculate their loyalty band, and add it to their data.
            # Boat loyalty is the number of times they have sailed this season, according to boat availability.
            # Sailor loyalty is the number of times they have sailed this season, according to sailor history,

            for available_boat_key in available_boat_keys:
                for boat_availability in database.boats_availability:
                    if available_boat_key == boat_availability["key"]:
                        loyalty = 0
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if boat_availability[date].upper() == 'Y':
                                loyalty += 1
                        for i in range(len(database.boats_data)):
                            if available_boat_key == database.boats_data[i]["key"]:
                                database.boats_data[i]["loyalty"] = str(loyalty)

            for available_sailor_key in available_sailor_keys:
                for sailor_history in database.sailor_histories:
                    loyalty = 0
                    if available_sailor_key == sailor_history["key"]:
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if sailor_history[date].upper() == 'Y':
                                loyalty += 1
                        for i in range(len(database.sailors_data)):
                            if available_sailor_key == database.sailors_data[i]["key"]:
                                database.sailors_data[i]["loyalty"] = str(loyalty)

            # For each available sailor, calculate their no_show status, and add it to their data.
            # no_show status is TRUE if their availability entry is 'N' for any date prior to the event_date.

            for available_sailor_key in available_sailor_keys:
                for sailors_availability in database.sailors_availability:
                    if available_sailor_key == sailors_availability["key"]:
                        no_show = "FALSE"
                        for date in constants.event_dates:
                            if sailors_availability[date].upper() == 'N':
                                no_show = "TRUE"
                                break
                            elif date == event_date:
                                break
                        for i in range(len(database.sailors_data)):
                            if available_sailor_key == database.sailors_data[i]["key"]:
                                database.sailors_data[i]["no_show"] = no_show

            # Form a new flotilla by applying the mandatory rules.

            extended_flotilla = mandatory.mandatory(available_boat_keys, available_sailor_keys)

            event = {}
            event["date"] = event_date
            event["flotilla"] = extended_flotilla["flotilla"]
            event["wait list"] = extended_flotilla["wait list"]


            # Modify the flotilla by applying the discretionary rules.

            if len(event["flotilla"]) > 1:
                event = discretionary.discretionary(event)

            # Update the addresses and crew information files with the data for the event date.

            addresses.add_boats(event)
            addresses.add_sailors(event)
            crew_info.add_info(event)

            # Update the sailor_histories file with the crew assignments for the event date.

            for crew in event["flotilla"]:
                for sailor in crew["sailors"]:
                    for sailor_history in database.sailor_histories:
                        if sailor_history["key"] == sailor:
                            sailor_history[event_date] = crew["boat"]

            # Add to the html file for all FUTURE event dates.

            database.html = crew_html.html(event)

    return

# --------------------------------------------------
