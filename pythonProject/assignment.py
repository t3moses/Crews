
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
    current_date = current_datetime.date()

    first_datetime = datetime.datetime.strptime(constants.event_ids[0], date_format)
    first_date = datetime.date(current_date.year, first_datetime.month, first_datetime.day)

    last_datetime = datetime.datetime.strptime(constants.event_ids[-1], date_format)
    last_date = datetime.date(current_date.year, last_datetime.month, last_datetime.day)

    if current_date > last_date: # You must be working on next year's calendar.
        current_date = first_date

    addresses.begin()
    crew_info.begin()

    random.seed(None)

    for event_id in constants.event_ids:

        event_datetime = datetime.datetime.strptime(event_id, date_format)
        event_date = datetime.date(current_date.year, event_datetime.month, event_datetime.day)

        if current_date <= event_date:

            print(event_id)

            record = {}
            record["date"] = event_id
            database.debug.append(record)

            addresses.add_date(event_id)

            random.seed(event_id)

            for sailor in database.sailor_histories:
                sailor[event_id] = ""

            # List the boats and sailors available on the event date.

            available_boat_keys = []  # list of boats available on the event date.
            for available_boat in database.boats_availability:
                if available_boat[event_id] == "Y":
                    available_boat_keys.append(available_boat["key"])

            available_sailor_keys = []  # list of sailors available on the event date.
            for available_sailor in database.sailors_availability:
                if available_sailor[event_id] == 'A':
                    available_sailor_keys.append(available_sailor["key"])
                    for sailor in database.sailors_data:
                        if sailor["key"] == available_sailor["key"]:
                            sailor["category"] = 'A'
                elif available_sailor[event_id] == 'G':
                    available_sailor_keys.append(available_sailor["key"])
                    for sailor in database.sailors_data:
                        if sailor["key"] == available_sailor["key"]:
                            sailor["category"] = 'G'
                elif available_sailor[event_id] == 'N':
                    available_sailor_keys.append(available_sailor["key"])
                    for sailor in database.sailors_data:
                        if sailor["key"] == available_sailor["key"]:
                            sailor["category"] = 'N'
                else:
                    pass

            # For each available boat and sailor, calculate their loyalty band, and add it to their data.
            # Boat loyalty is the number of times they have sailed this season, according to boat availability.
            # Sailor loyalty is the number of times they have sailed this season, according to sailor history,

            for available_boat_key in available_boat_keys:
                for boat_availability in database.boats_availability:
                    if available_boat_key == boat_availability["key"]:
                        loyalty = 0
                        for date in constants.event_ids:
                            if date == event_id:
                                break
                            if boat_availability[date] == 'Y':
                                loyalty += 1
                        for i in range(len(database.boats_data)):
                            if available_boat_key == database.boats_data[i]["key"]:
                                database.boats_data[i]["loyalty"] = str(loyalty)

            for available_sailor_key in available_sailor_keys:
                for sailor_history in database.sailor_histories:
                    loyalty = 0
                    if available_sailor_key == sailor_history["key"]:
                        for date in constants.event_ids:
                            if date == event_id:
                                break
                            if not sailor_history[date] == '':
                                loyalty += 1
                        for i in range(len(database.sailors_data)):
                            if available_sailor_key == database.sailors_data[i]["key"]:
                                database.sailors_data[i]["loyalty"] = str(loyalty)

            # Form a new flotilla by applying the mandatory rules.

            extended_flotilla = mandatory.mandatory(available_boat_keys, available_sailor_keys)

            event = {}
            event["date"] = event_id
            event["flotilla"] = extended_flotilla["flotilla"]
            event["wait list"] = extended_flotilla["wait list"]

            # If the days to the event date are less than the cut_off, set the sailors' availability to 'G'
            # and the wait-list to 'A'.

            if (event_date - current_date).days <= constants.cut_off:
                for crew in event["flotilla"]:
                    for sailor_key in crew["sailors"]:
                        for i in range(len(database.sailors_availability)):
                            if database.sailors_availability[i]["key"] == sailor_key:
                                database.sailors_availability[i][event_id] = 'G'

                for sailor_key in event["wait list"]:
                    for i in range(len(database.sailors_availability)):
                        if database.sailors_availability[i]["key"] == sailor_key:
                            database.sailors_availability[i][event_id] = 'A'

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
                            sailor_history[event_id] = crew["boat"]

            # Add to the html file for all FUTURE event dates.

            database.html = crew_html.html(event)

    return

# --------------------------------------------------
