
import database
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

    for event_date in constants.event_dates:

        event_datetime = datetime.datetime.strptime(event_date, date_format)

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

            for available_sailor in available_sailors:
                print(available_sailor["key"], available_sailor["loyalty"])

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

            for iteration in range(constants.outer_epochs):

                random.seed(event_date + "v" + str(iteration))

                # Form crews by applying the mandatory and discretionary rules.

                assignments = mandatory.mandatory(available_boats, available_sailors)
                crews = assignments["crews"]
                wait_list = assignments["wait list"]

                if len(crews) >= 2:
                    crews = discretionary.discretionary(crews, database.sailor_histories, event_date)

                if iteration == 0:
                    best_crews = crews
                    best_score = int(crews["crews score"])
                elif int(crews["crews score"]) < best_score:
                    best_crews = crews
                    best_score = int(crews["crews score"])
                else: pass

            # Update the sailor_histories file with the crew assignments for the event date.

            for crew in best_crews["crews"]:
                for sailor in crew["sailors"]:
                    for sailor_history in database.sailor_histories:
                        if sailor_history["key"] == sailor["key"]:
                            sailor_history[event_date] = crew["boat"]["key"]

            database.html = crew_html.html(best_crews, wait_list, event_date)

    return
