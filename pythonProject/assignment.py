
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

        database.debug += "\nEvent date: " + event_date + "\n\n"
        addresses.add_date(event_date)

        event_datetime = datetime.datetime.strptime(event_date, date_format)

        random.seed(event_date)

        if current_datetime <= event_datetime:

            for sailor in database.sailor_histories:
                sailor[event_date] = ""

            # List the boats and sailors available on the event date.

            available_boats = []  # list of boats available on the event date.
            for available_boat in database.boats_availability:
                if not available_boat[event_date] == "":
                    for boat in database.boats_data:
                        if available_boat["key"] == boat["key"]:
                            available_boats.append(boat["key"])

            available_sailors = []  # list of sailors available on the event date.
            for available_sailor in database.sailors_availability:
                if not available_sailor[event_date] == '':
                    for sailor in database.sailors_data:
                        if available_sailor["key"] == sailor["key"]:
                            available_sailors.append(sailor["key"])

            # For each available boat and sailor, calculate their loyalty band, and add it to their data.
            # Boat loyalty is the number of times they have sailed this season, according to boat availability.
            # Sailor loyalty is the number of times they have sailed this season, according to sailor history,

            for available_boat in available_boats:
                for boat_availability in database.boats_availability:
                    if available_boat == boat_availability["key"]:
                        loyalty = 0
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if not boat_availability[date] == '':
                                loyalty += 1
                        for i in range(len(database.boats_data)):
                            if available_boat == database.boats_data[i]["key"]:
                                database.boats_data[i]["loyalty"] = str(loyalty)

            for available_sailor in available_sailors:
                for sailor_history in database.sailor_histories:
                    loyalty = 0
                    if available_sailor == sailor_history["key"]:
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if not sailor_history[date] == '':
                                loyalty += 1
                        for i in range(len(database.sailors_data)):
                            if available_sailor == database.sailors_data[i]["key"]:
                                database.sailors_data[i]["loyalty"] = str(loyalty)

            # Form a new flotilla by applying the mandatory rules.

            extended_flotilla = mandatory.mandatory(available_boats, available_sailors)

            event = {}
            event["date"] = event_date
            event["flotilla"] = extended_flotilla["flotilla"]
            event["wait list"] = extended_flotilla["wait list"]

            addresses.add_boats(event)
            addresses.add_sailors(event)
            crew_info.add_info(event)

            # Modify the flotilla by applying the discretionary rules.

            event = discretionary.discretionary(event)

            # Update the sailor_histories file with the crew assignments for the event date.

            for crew in event["flotilla"]:
                for sailor in crew["sailors"]:
                    for sailor_history in database.sailor_histories:
                        if sailor_history["key"] == sailor:
                            sailor_history[event_date] = crew["boat"]

            # Add to the html file for all FUTURE event dates.

            database.html = crew_html.html(event)

    return
