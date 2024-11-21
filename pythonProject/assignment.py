#!.venv/bin/python3.12

import csv
import random
import datetime
import constants
import mandatory
import discretionary
import crew_html

crew_html.begin()

Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/"

with open(Working_directory + "Config/" + "config.txt", "r") as f_config:
    s_line_1 = f_config.readline()  # boats data
    s_line_2 = f_config.readline()  # sailors data
    s_line_3 = f_config.readline()  # boats availability
    s_line_4 = f_config.readline()  # sailors availability
    s_line_5 = f_config.readline()  # sailors history
    s_line_6 = f_config.readline()  # user input form
    s_line_7 = f_config.readline()  # events path

boats_data_filename = Working_directory+s_line_1.split(': ')[1].split(' //')[0]
sailors_data_filename = Working_directory+s_line_2.split(': ')[1].split(' //')[0]
boats_availability_filename = Working_directory+s_line_3.split(': ')[1].split(' //')[0]
sailors_availability_filename = Working_directory+s_line_4.split(': ')[1].split(' //')[0]
sailor_histories_filename = Working_directory+s_line_5.split(': ')[1].split(' //')[0]
user_input_form_filename = s_line_6.split(': ')[1].split(' //')[0]
events_path = s_line_7.split(': ')[1].split(' //')[0]

# Get boats_data (the list of boat data dictionaries), as this is the authoritative source of boat names.

boats_data = []
with open(boats_data_filename) as boats_data_file:
    for boat in csv.DictReader(boats_data_file):
        boats_data.append(boat)

# Get sailors_data (the list of sailor data dictionaries), as this is the authoritative source of sailor names.

sailors_data = []  # list of sailor data dictionaries.
with open(sailors_data_filename) as sailors_data_file:
    for sailor in csv.DictReader(sailors_data_file):
        sailors_data.append(sailor)

# Create the header row of the CSV files.

boat_header_row = ["boat name"] + constants.event_dates
sailor_header_row = ["display name"] + constants.event_dates

# Open the boat availability file.  If it doesn't yet exist, create it.
# Then write a list of dictionaries containing the name of each boat from the boat_data.

try:
    boats_availability_file = open(boats_availability_filename, 'r', newline='')
except FileNotFoundError:
    print("Creating boats availability file.")
    boats_availability_file = open(boats_availability_filename, 'w+', newline='')
    writer = csv.DictWriter(boats_availability_file, fieldnames=boat_header_row)
    writer.writeheader()
    for boat in boats_data:
        writer.writerow({"boat name": boat["boat name"]})
boats_availability_file.close()

# Create boats_availability (the list of boat availability dictionaries) from file.

boats_availability = []
with open(boats_availability_filename) as boats_availability_file:
    reader = csv.DictReader(boats_availability_file)
    for boat in reader:
        boats_availability.append(boat)

# Confirm that boat names are consistent between the boats_availability and boat_data files.

boats_from_availability = []
for boat in boats_availability:
    boats_from_availability.append(boat["boat name"])
boats_from_data = []
for boat in boats_data:
    boats_from_data.append(boat["boat name"])
if bool(set(boats_from_availability) ^ set(boats_from_data)):
    raise Exception("Boat availability is inconsistent with boat data.")

# Open the sailors availability file.  If it doesn't yet exist, create it.
# Then write a list of dictionaries containing the name of each sailor from the sailor_data.

try:
    sailors_availability_file = open(sailors_availability_filename, 'r', newline='')
except FileNotFoundError:
    print("Creating sailors availability file.")
    sailors_availability_file = open(sailors_availability_filename, 'w+', newline='')
    writer = csv.DictWriter(sailors_availability_file, fieldnames=sailor_header_row)
    writer.writeheader()
    for sailor in sailors_data:
        # writer.writerow({"display name": sailor["display name"]})
        writer.writerow({"display name": sailor[0]})
sailors_availability_file.close()

# Create sailors_availability (the list of sailor availability dictionaries) from file.

sailors_availability = []
with open(sailors_availability_filename) as sailors_availability_file:
    reader = csv.DictReader(sailors_availability_file)
    for sailor in reader:
        sailors_availability.append(sailor)

# Confirm that sailor names are consistent between the sailor_availability and sailor_data files.

sailors_from_availability = []
for sailor in sailors_availability:
    sailors_from_availability.append(sailor["display name"])
sailors_from_data = []
for sailor in sailors_data:
    sailors_from_data.append(sailor["display name"])
if bool(set(sailors_from_availability) ^ set(sailors_from_data)):
    raise Exception("Sailor availability is inconsistent with sailor data.")

# Confirm that sailor whitelists are consistent with boats_sata.

boats_from_data = []
for boat in boats_data:
    boats_from_data.append(boat["boat name"])
for sailor in sailors_data:
    sailor_whitelist = sailor["whitelist"].split(";")

    if not bool(set(sailor_whitelist) <= set(boats_from_data)):
        raise Exception("Sailor whitelist is inconsistent with boat data.")

# Check that event dates from boat_availability and sailor_availability are consistent.

sailor_dates = list(sailors_availability[1].keys())
sailor_dates.remove('display name')
if bool(set(sailor_dates) ^ set(constants.event_dates)):
    raise Exception("Sailor availability is inconsistent with boat availability.")

# Open the sailor histories file.  If it doesn't yet exist, create it and write a list of dictionaries
# containing the name of each sailor from the sailor_data.

try:
    sailor_histories_file = open(sailor_histories_filename, 'r', newline='')
except FileNotFoundError:
    print("Creating sailor histories file.")
    sailor_histories_file = open(sailor_histories_filename, 'w+', newline='')
    writer = csv.DictWriter(sailor_histories_file, fieldnames=sailor_header_row)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow({"display name": sailor["display name"]})

sailor_histories_file.close()

# Create sailor_histories (the list of sailor history dictionaries) from file.

sailor_histories = []
with open(sailor_histories_filename, mode='r') as sailor_histories_file:
    reader = csv.DictReader(sailor_histories_file)
    for sailor_history in reader:
        sailor_histories.append(sailor_history)

# Set current_datetime no later than the last event date.

date_format = '%a %b %d'
current_datetime = datetime.datetime.now()
first_date = datetime.datetime.strptime(constants.event_dates[0], date_format)
last_date = datetime.datetime.strptime(constants.event_dates[-1], date_format)
if current_datetime > last_date:
    current_datetime = first_date

for event_date in constants.event_dates:

    event_datetime = datetime.datetime.strptime(event_date, date_format)

    if current_datetime <= event_datetime:

        # List the boats and sailors available on the event date.

        available_boats = []  # list of dictionaries for boats available on the event date.
        for available_boat in boats_availability:
            if not available_boat[event_date] == '':
                for boat in boats_data:
                    if boat["boat name"] == available_boat["boat name"]:
                        available_boats.append(boat)

        available_sailors = []  # list of dictionaries for sailors available on the given date.
        for available_sailor in sailors_availability:
            if not available_sailor[event_date] == '':
                for sailor in sailors_data:
                    if sailor["display name"] == available_sailor["display name"]:
                        available_sailors.append(sailor)

        # For each available sailor and boat, calculate their loyalty band, and add it to their data.
        # Sailor loyalty is derived from sailor_history, whereas boat_loyalty is derived from boat_availability.

        for available_sailor in available_sailors:
            for sailor_history in sailor_histories:
                loyalty = 0
                if available_sailor["display name"] == sailor_history["display name"]:
                    for date in constants.event_dates:
                        if date == event_date:
                            break
                        if not sailor_history[date] == '':
                            loyalty += 1
                    available_sailor["loyalty"] = [str(loyalty) for sailor in available_sailors if sailor["display name"] == available_sailor["display name"]][0]

        for available_boat in available_boats:
            for boat_availability in boats_availability:
                if boat_availability["boat name"] == available_boat["boat name"]:
                    loyalty = 0
                    for date in constants.event_dates:
                        if date == event_date:
                            break
                        if not boat_availability[date] == '':
                            loyalty += 1
                    available_boat["loyalty"] = loyalty

        for iteration in range(constants.outer_epochs):

            random.seed(event_date + "v" + str(iteration))

            # Form crews by applying the mandatory and discretionary rules.

            assignments = mandatory.mandatory(available_boats, available_sailors)
            crews = assignments["crews"]
            wait_list = assignments["wait_list"]

            if len(crews) >= 2:
                crews = discretionary.discretionary(crews, sailor_histories, event_date)

            if iteration == 0:
                best_crews = crews
                best_score = int(crews["crews score"])
                trial = 0
            elif int(crews["crews score"]) < best_score:
                best_crews = crews
                best_score = int(crews["crews score"])
                trial = iteration
            else: pass

        # Update the sailor_histories file with the crew assignments for the event date.

        for crew in best_crews["crews"]:
            for sailor in crew["sailors"]:
                for sailor_history in sailor_histories:
                    if sailor_history["display name"] == sailor["display name"]:
                        sailor_history[event_date] = crew["boat"]["boat name"]

        # Write sailor_histories to file.

        sailor_histories_file = open(sailor_histories_filename, 'w', newline='')

        writer = csv.DictWriter(sailor_histories_file, fieldnames=sailor_header_row)
        writer.writeheader()
        for sailor_history in sailor_histories:
            writer.writerow(sailor_history)

        sailor_histories_file.close()

    # Output a string containing the html for the crews.

    html = crew_html.html(best_crews, wait_list, event_date)

events_file = open(Working_directory + "html/assignments.html", 'w+', newline='')
events_file.write(html)
events_file.close()
