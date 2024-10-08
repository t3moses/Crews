#!.venv/bin/python3.12

import csv
import assign

print()
event_date = input("Enter date (MM-DD):")
print("Date: ", event_date)

Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/Config/"

with open(Working_directory+"config.txt", "r") as f_config:
    s_line_1 = f_config.readline() # boats data
    s_line_2 = f_config.readline() # sailors data
    s_line_3 = f_config.readline() # boats availability
    s_line_4 = f_config.readline() # sailors availability
    s_line_5 = f_config.readline() # sailors history

boats_data_filename = Working_directory+s_line_1.split(': ')[1].split(' //')[0]
sailors_data_filename = Working_directory+s_line_2.split(': ')[1].split(' //')[0]
boats_availability_filename = Working_directory+s_line_3.split(': ')[1].split(' //')[0]
sailors_availability_filename = Working_directory+s_line_4.split(': ')[1].split(' //')[0]
sailor_histories_filename = Working_directory+s_line_5.split(': ')[1].split(' //')[0]

boats_data = [] # list of boat data dictionaries.
with open(boats_data_filename) as boats_data_file:
    for boat in csv.DictReader(boats_data_file):
        boats_data.append(boat)

boats_availability = [] # list of boat availability dictionaries.
with open(boats_availability_filename) as boats_availability_file:
    for boat in csv.DictReader(boats_availability_file):
        boats_availability.append(boat)

available_boats = [] # list of dictionaries for boats available on the event date.
for available_boat in boats_availability:
    if not available_boat[event_date] == '':
        for boat in boats_data:
            if boat["name"] == available_boat["name"]:
                available_boats.append(boat)

sailors_data = [] # list of sailor data dictionaries.
with open(sailors_data_filename) as sailors_data_file:
    for sailor in csv.DictReader(sailors_data_file):
        sailors_data.append(sailor)

sailors_availability = [] # list of sailor availability dictionaries.
with open(sailors_availability_filename) as sailors_availabliity_file:
    for sailor in csv.DictReader(sailors_availabliity_file):
        sailors_availability.append(sailor)

available_sailors = [] # list of dictionaries for sailors available on the given date.
for available_sailor in sailors_availability:
    if not available_sailor[event_date] == '':
        for sailor in sailors_data:
            if sailor["name"] == available_sailor["name"]:
                available_sailors.append(sailor)

event_dates = list(sailors_availability[1].keys()) # list of event dates as str
event_dates.remove('name')

# Open the sailor histories file.  If it doesn't yet exist, create it and write a list of dictionaries
# containing the name of each sailor from the sailor_data.

try:
    sailor_histories_file = open(sailor_histories_filename, 'r+', newline='')
except FileNotFoundError:
    sailor_histories_file = open(sailor_histories_filename, 'w+', newline='')
    writer = csv.DictWriter(sailor_histories_file, fieldnames=event_dates)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow({"name": sailor["name"]})

# Populate the sailor_histories list from the sailor_histories_file.

sailor_histories = [] # list of dictionaries containing the history of boats to which each sailor
# has been assigned in previous events.

for sailor_history in csv.DictReader(sailor_histories_file):
    sailor_histories.append(sailor_history)

sailor_histories_file.close()

# For each available sailor and boat, calculate their loyalty level, and add it to their data.

for i in range(len(sailor_histories)):
    sailor_history = sailor_histories[i]
    loyalty = 0
    for date in event_dates:
        if date == event_date:
           break
        if not sailor_history[date] == '':
            loyalty += 1
    sailors_data[i]["loyalty"] = str(loyalty)

for i in range(len(boats_availability)):
    boat_availability = boats_availability[i]
    loyalty = 0
    for date in event_dates:
        if date == event_date:
           break
        if not boat_availability[date] == '':
            loyalty += 1
    boats_data[i]["loyalty"] = str(loyalty)

crews = assign.assign(available_boats, available_sailors)
