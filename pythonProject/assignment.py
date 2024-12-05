
import copy
import database
import addresses
import random
import datetime
import constants
import mandatory
import discretionary
import crew_html

def assignment():

    date_format = '%a %b %d'
    current_datetime = datetime.datetime.now()
    first_date = datetime.datetime.strptime(constants.event_dates[0], date_format)
    last_date = datetime.datetime.strptime(constants.event_dates[-1], date_format)
    if current_datetime > last_date:
        current_datetime = first_date

    addresses.begin()

    random.seed(None)

    for event_date in constants.event_dates:

        database.debug += event_date + "\n\n"
        addresses.add_date(event_date)

        event_datetime = datetime.datetime.strptime(event_date, date_format)

        random.seed(event_date)

        if current_datetime <= event_datetime:

            for sailor in database.sailor_histories:
                sailor[event_date] = ""

            # List the boats and sailors available on the event date.

            available_boats = []  # list of dictionaries for boats available on the event date.
            for available_boat in database.boats_availability:
                if not available_boat[event_date] == "":
                    for boat in database.boats_data:
                        if boat["key"] == available_boat["key"]:
                            available_boats.append(boat.copy())

            available_sailors = []  # list of dictionaries for sailors available on the given date.
            for available_sailor in database.sailors_availability:
                if not available_sailor[event_date] == '':
                    for sailor in database.sailors_data:
                        if sailor["key"] == available_sailor["key"]:
                            available_sailors.append(sailor.copy())

            # For each available sailor and boat, calculate their loyalty band, and add it to their data.
            # Sailor loyalty is derived from sailor_history, whereas boat_loyalty is derived from boat_availability.

            for available_sailor in available_sailors:
                for sailor_history in database.sailor_histories:
                    loyalty = 0
                    if available_sailor["key"] == sailor_history["key"]:
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if not sailor_history[date] == '':
                                loyalty += 1
                        available_sailor["loyalty"] = str(loyalty)

            for available_boat in available_boats:
                for boat_availability in database.boats_availability:
                    if boat_availability["key"] == available_boat["key"]:
                        loyalty = 0
                        for date in constants.event_dates:
                            if date == event_date:
                                break
                            if not boat_availability[date] == '':
                                loyalty += 1
                        available_boat["loyalty"] = str(loyalty)

            # Form a new flotilla by applying the mandatory rules using the updated random seed.

            flotilla = mandatory.mandatory(available_boats, available_sailors)

            addresses.add_boats(flotilla)
            addresses.add_sailors(flotilla)

            for iteration in range(constants.outer_epochs):

                random.seed(event_date + "v" + str(iteration))

                flotilla = mandatory.reassign(flotilla)

                if len(flotilla["crews"]) < 2:
                    best_flotilla = copy.deepcopy(flotilla)
                    break

                # Modify the flotilla by applying the discretionary rules.
                # The resulting flotilla includes its score.

                flotilla = discretionary.discretionary(flotilla, event_date)

                if iteration == 0:
                    best_flotilla = copy.deepcopy(flotilla)
                    best_score = int(flotilla["score"])
                else:
                    if int(flotilla["score"]) < best_score:
                        best_flotilla = copy.deepcopy(flotilla)
                        best_score = int(flotilla["score"])

            # Update the sailor_histories file with the crew assignments for the event date.

            for crew in best_flotilla["crews"]:
                for sailor in crew["sailors"]:
                    for sailor_history in database.sailor_histories:
                        if sailor_history["key"] == sailor["key"]:
                            sailor_history[event_date] = crew["boat"]["key"]

            # Add to the html file for all FUTURE event dates.

            database.html = crew_html.html(best_flotilla, event_date)

    return
