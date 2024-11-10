#!.venv/bin/python3.12

import csv
import constants

def value_from_form(form, field_name):

    # Return the value of the named field from the form.

    if not form.find(field_name) == -1:
        return (form.rpartition(field_name)[2]).rsplit("\n")[0]
    else:
        return ""

def enrol_boat(form):

    # Add the boat described by the form to the boats data file
    # and the sailor whitelists.

    boats_data_filename = Working_directory + s_line_1.split(': ')[1].split(' //')[0]
    boats_data = [] # List of boat names.
    with open(boats_data_filename, mode='r') as boats_data_file:
        for boat in csv.DictReader(boats_data_file):
            boats_data.append(boat)

    sailors_data_filename = Working_directory + s_line_2.split(': ')[1].split(' //')[0]
    sailors_data = []  # list of sailor data dictionaries.
    with open(sailors_data_filename, mode='r') as sailors_data_file:
        for sailor in csv.DictReader(sailors_data_file):
            sailors_data.append(sailor)

    boat_field_names = boats_data[0].keys()
    sailor_field_names = sailors_data[0].keys()

    # Process new boat data from the form.

    boat_name = value_from_form(form, "Boat name: ")
    email_address = value_from_form(form, "Email: ")
    min_occupancy = value_from_form(form, "Minimum number of crew: ")
    max_occupancy = value_from_form(form, "Maximum number of crew: ")
    if value_from_form(form, "experienced sailor in the crew: ") == "Checked":
        request_assist = "True"
    else:
        request_assist = "False"

    # If an entry for the boat already exists, delete it.
    # Otherwise, add the boat name to all sailor whitelists.

    for boat in boats_data:
        if boat["boat name"] == boat_name:
            boats_data.remove(boat)

    for sailor in sailors_data:
        if sailor["whitelist"].count(boat_name) == 0:
            sailor["whitelist"] = sailor["whitelist"] + " " + boat_name

    new_boat = {}

    new_boat["boat name"] = boat_name
    new_boat["owner email address"] = email_address
    new_boat["min_occupancy"] = min_occupancy
    new_boat["max_occupancy"] = max_occupancy
    new_boat["request assist"] = request_assist

    # Add the new boat to the boats data file
    # and update the boats data file.

    boats_data.append(new_boat)

    boats_data_file = open(boats_data_filename, 'w', newline='')
    writer = csv.DictWriter(boats_data_file, fieldnames=boat_field_names)
    writer.writeheader()
    for boat in boats_data:
        writer.writerow(boat)
    boats_data_file.close()

    # Update the sailors data file.

    sailors_data_file = open(sailors_data_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_data_file, fieldnames=sailor_field_names)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow(sailor)
    sailors_data_file.close()

    return


def enrol_sailor(form):

    # Add the sailor described by the form to the sailors data file and sailors history file.

    sailors_data_filename = Working_directory + s_line_2.split(': ')[1].split(' //')[0]
    sailors_data = []  # list of sailor data dictionaries.
    with open(sailors_data_filename, mode='r') as sailors_data_file:
        for sailor in csv.DictReader(sailors_data_file):
            sailors_data.append(sailor)

    sailor_field_names = sailors_data[0].keys()

    sailor_histories_filename = Working_directory + s_line_5.split(': ')[1].split(' //')[0]
    sailors_history = []  # list of sailor history dictionaries.
    with open(sailor_histories_filename, mode='r') as sailor_histories_file:
        for sailor in csv.DictReader(sailor_histories_file):
            sailors_history.append(sailor)

    history_field_names = sailors_history[0].keys()

    boats_data_filename = Working_directory + s_line_1.split(': ')[1].split(' //')[0]
    boat_list = [] # List of boat names.
    with open(boats_data_filename, mode='r') as boats_data_file:
        for boat in csv.DictReader(boats_data_file):
            boat_list.append(boat["boat name"])

    boat_names = ""
    for i in range(len(boat_list)):
        if not i == 0:
            boat_names += ";"
        boat_names += boat_list[i]

    # Process the enrol sailor form data.

    first_name = value_from_form(form, "First name: ")
    last_name = value_from_form(form, "Last name: ")
    email_address = value_from_form(form, "Email: ")
    membership_number = value_from_form(form, "NSC membership number: ")
    background = value_from_form(form, "Background: ")
    experience = value_from_form(form, "experience: ")

    display_name = first_name.capitalize() + " " + last_name.capitalize()[0]
    if membership_number == "":
        member = "False"
    else:
        member = "True"
    if value_from_form(form, "space allows: ") == "Checked":
        request_female = "True"
    else:
        request_female = "False"
    if background == "I am new to sailing":
        skill = 0
    elif background == "I have a basic qualification":
        skill = 1
    elif background == "I am an experienced sailor":
        skill = 2
    else:
        skill = 0

    # If an entry for the sailor already exists, delete it from sailors data and sailors history.

    for sailor in sailors_data:
        if sailor["display name"] == display_name:
            sailors_data.remove(sailor)

    for sailor in sailors_history:
        if sailor["display name"] == display_name:
            sailors_history.remove(sailor)

    new_sailor = {}

    new_sailor["display name"] = display_name
    new_sailor["email address"] = email_address
    new_sailor["member"] = member
    new_sailor["skill"] = skill
    new_sailor["experience"] = experience
    new_sailor["request female"] = request_female
    new_sailor["whitelist"] = boat_names

    new_history = {}
    new_history["display name"] = display_name
    for event_date in constants.event_dates:
        new_history[event_date] = ""

    # Add the new sailor to sailors data and sailors history.

    sailors_data.append(new_sailor)
    sailors_history.append(new_history)

    # Update the sailors data file and sailors history file.

    sailors_data_file = open(sailors_data_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_data_file, fieldnames=sailor_field_names)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow(sailor)
    sailors_data_file.close()

    sailors_history_file = open(sailor_histories_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_history_file, fieldnames=history_field_names)
    writer.writeheader()
    for sailor in sailors_history:
        writer.writerow(sailor)
    sailors_history_file.close()

    return


def register_boat(form):

    # Update the boats availability file with the information in the form.

    boats_availability_filename = Working_directory + s_line_3.split(': ')[1].split(' //')[0]
    boats_availability = []
    with open(boats_availability_filename) as boats_availability_file:
        reader = csv.DictReader(boats_availability_file)
        for boat in reader:
            boats_availability.append(boat)

    boat_field_names = boats_availability[0].keys()

    boat_name = value_from_form(form, "Boat name: ")

    # Update the boats availability file.

    for boat in boats_availability:
        if boat["boat name"] == boat_name:
            for event_date in constants.event_dates:
                if value_from_form(form, event_date + ": ") == "Register":
                    boat[event_date] = "Y"
                if value_from_form(form, event_date + ": ") == "Cancel":
                    boat[event_date] = ""

    boats_availability_file = open(boats_availability_filename, 'w', newline='')
    writer = csv.DictWriter(boats_availability_file, fieldnames=boat_field_names)
    writer.writeheader()
    for boat in boats_availability:
        writer.writerow(boat)
    boats_availability_file.close()

    return


def register_sailor(form):

    # Update the sailor availability file with the information in the form.

    sailors_availability_filename = Working_directory + s_line_4.split(': ')[1].split(' //')[0]
    sailors_availability = []
    with open(sailors_availability_filename) as sailors_availability_file:
        reader = csv.DictReader(sailors_availability_file)
        for sailor in reader:
            sailors_availability.append(sailor)

    sailor_field_names = sailors_availability[0].keys()

    first_name = value_from_form(form, "First name: ")
    last_name = value_from_form(form, "Last name: ")
    display_name = first_name.capitalize() + " " + last_name.capitalize()[0]

    for sailor in sailors_availability:
        if sailor["display name"] == display_name:
            for event_date in constants.event_dates:
                if value_from_form(form, event_date + ": ") == "Register":
                    sailor[event_date] = "Y"
                if value_from_form(form, event_date + ": ") == "Cancel":
                    sailor[event_date] = ""

    # Update the sailors availability file.

    sailors_availability_file = open(sailors_availability_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_availability_file, fieldnames=sailor_field_names)
    writer.writeheader()
    for boat in sailors_availability:
        writer.writerow(boat)
    sailors_availability_file.close()

    return


Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/"

with open(Working_directory + "Config/" + "config.txt", "r") as f_config:
    s_line_1 = f_config.readline()  # boats data
    s_line_2 = f_config.readline()  # sailors data
    s_line_3 = f_config.readline()  # boats availability
    s_line_4 = f_config.readline()  # sailors availability
    s_line_5 = f_config.readline()  # sailors history
    s_line_6 = f_config.readline()  # user input form
    s_line_7 = f_config.readline()  # events path

user_input_form_filename = Working_directory+s_line_6.split(': ')[1].split(' //')[0]

form_file = open(user_input_form_filename, "r")
form = form_file.read()
form_file.close()

form_name = value_from_form(form, "Form name: ")

if form_name == "Enrol boat":
    enrol_boat(form)
elif form_name == "Enrol sailor":
    enrol_sailor(form)
elif form_name == "Register boat":
    register_boat(form)
elif form_name == "Register sailor":
    register_sailor(form)
else:
    raise Exception("Unrecognised form.")
