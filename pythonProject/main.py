#!.venv/bin/python3.12

import csv
import mandatory
import discretionary

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

# Get boats_data, the list of boat data dictionaries, as this is the authoritative source of boat names.

boats_data = []
with open(boats_data_filename) as boats_data_file:
    for boat in csv.DictReader(boats_data_file):
        boats_data.append(boat)

# Get sailors_data, the list of sailor data dictionaries, as this is the authoritative source of sailor names.

sailors_data = []  # list of sailor data dictionaries.
with open(sailors_data_filename) as sailors_data_file:
    for sailor in csv.DictReader(sailors_data_file):
        sailors_data.append(sailor)

# Get boats_availability, the list of boat availability dictionaries, as this is the authoritative source of event dates.

boats_availability = []
with open(boats_availability_filename) as boats_availability_file:
    for boat in csv.DictReader(boats_availability_file):
        boats_availability.append(boat)

# Get sailors_availability, the list of sailor availability dictionaries.

sailors_availability = []
with open(sailors_availability_filename) as sailors_availabliity_file:
    for sailor in csv.DictReader(sailors_availabliity_file):
        sailors_availability.append(sailor)

# Confirm that boat names are consistent between the boat_availability and boat_data files.

list1 = []
for boat in boats_availability:
    list1.append(boat["name"])
list2 = []
for boat in boats_data:
    list2.append(boat["name"])
if bool(set(list1) - set(list2)):
    raise Exception("Boat availability is inconsistent with boat data.")

# Confirm that sailor names are consistent between the sailor_availability and sailor_data files.

list1 = []
for sailor in sailors_availability:
    list1.append(sailor["name"])
list2 = []
for sailor in sailors_data:
    list2.append(sailor["name"])
if bool(set(list1) - set(list2)):
    raise Exception("Sailor availability is inconsistent with sailor data.")

# Take the event dates from boats_availability.
# Get the event date from the user and check that it is in the set of event dates.

event_dates = list(boats_availability[1].keys())
event_dates.remove('name')

print()
event_date = input("Enter date (MM-DD):")
print("Date: ", event_date)

if event_dates.count(event_date) == 0:
    raise Exception("Invalid event date")

# Check that event dates from boat_availability and sailor_availability are consistent.

sailor_dates = list(sailors_availability[1].keys())
sailor_dates.remove('name')
set1 = set(sailor_dates)
set2 = set(event_dates)
if bool(set1 - set2):
    raise Exception("Sailor availability is inconsistent with boat availability.")

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

# list of dictionaries containing the history of boats to which each sailor
# has been assigned in previous events.
# Populate the sailor_histories list from the sailor_histories_file.

sailor_histories = []
for sailor_history in csv.DictReader(sailor_histories_file):
    sailor_histories.append(sailor_history)

sailor_histories_file.close()

# List the boats and sailors available on the event date.

available_boats = [] # list of dictionaries for boats available on the event date.
for available_boat in boats_availability:
    if not available_boat[event_date] == '':
        for boat in boats_data:
            if boat["name"] == available_boat["name"]:
                available_boats.append(boat)

available_sailors = [] # list of dictionaries for sailors available on the given date.
for available_sailor in sailors_availability:
    if not available_sailor[event_date] == '':
        for sailor in sailors_data:
            if sailor["name"] == available_sailor["name"]:
                available_sailors.append(sailor)

# For each available sailor and boat, calculate their loyalty band, and add it to their data.

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

# Form crews by applying the mandatory and discretionary rules.

crews = mandatory.mandatory(available_boats, available_sailors)

crews = discretionary.discretionary(crews, sailor_histories, event_date)

# Update sailor_histories with the crew assignments.

for crew in crews:
    for sailor in crew["sailors"]:
        for history in range(len(sailor_histories)):
            if sailor_histories[history]["name"] == sailor["name"]:
                sailor_histories[history][event_date] = crew["boat"]["name"]
for history in range(len(sailor_histories)):
    print(sailor_histories[history])

# Write sailor_histories to file.
