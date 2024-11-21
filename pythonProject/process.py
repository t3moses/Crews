#!.venv/bin/python3.12

import assignment
import csv
import constants

def single_line_from_form(form, field_name):

    # Return the value of the named field from the form.
    # If the named field is not present in the form, return an empty string.
    # Otherwise, return the contents of the form between the field name and the end of the line.

    if not form.find(field_name) == -1:
        return (form.rpartition(field_name)[2]).rsplit("\n")[0]
    else:
        return ""

def multi_line_from_form(form, field_name):

    # Return the value of the named field from the form.
    # If the named field is not present in the form, return an empty string.
    # Otherwise, return the contents of the form between the field name and the first : character.
    # Delete the portion from the last new line (inclusive) to the end.

    if not form.find(field_name) == -1:
        new_field = form.rpartition(field_name)[2].rsplit(":")[0]
        new_field = new_field.rpartition("\n")[0]
        return new_field
    else:
        return ""

def no_new_line(string):

    # The string may be used in a CSV file, so remove all new lines.

    no_new_line_string = ""
    for i in range(len(string)):
        if ord(string[i]) == 10:
            no_new_line_string += "&#10;"
        else:
            no_new_line_string += string[i]
    return no_new_line_string

def no_comma(string):

    # The string may be used in a CSV file, so remove all commas.

    no_comma_string = ""
    for i in range(len(string)):
        if string[i] == ",":
            no_comma_string += "&#44;"
        else:
            no_comma_string += string[i]
    return no_comma_string

def canonicalize(string):

    # Remove leading and trailing spaces.
    # Convert the input to lower case.
    # Then capitalize the first letter of each word.

    new_string = no_comma(string).strip().casefold().title()

    return new_string

def remove_dict(list, key, value):

    # Return the list of dictionaries having removed all entries containing the key:value pair.

    indices = []
    for i in range(len(list)):
        if list[i][key] == value:
            indices.append(i)
    indices.reverse()
    for j in range(len(indices)):
        list.pop(indices[j])
    return list

def sailor_unavailable(boat_name, event_date):

    # If the owner of the boat is scheduled to be a sailor on the event date, then
    # his sailing registration is cancelled.

    # Open the bpat data and sailor availability files.

    boats_data_filename = Working_directory + s_line_1.split(': ')[1].split(' //')[0]
    boats_data = [] # List of boat names.
    with open(boats_data_filename, mode='r') as boats_data_file:
        for boat in csv.DictReader(boats_data_file):
            boats_data.append(boat)

    sailors_available_filename = Working_directory + s_line_4.split(': ')[1].split(' //')[0]
    sailors_available = []  # list of sailor availability dictionaries.
    with open(sailors_available_filename, mode='r') as sailors_available_file:
        for sailor in csv.DictReader(sailors_available_file):
            sailors_available.append(sailor)

    available_field_names = sailors_available[0].keys()

    for boat in boats_data:
        if boat["boat name"] == boat_name:
            for sailor_available in sailors_available:
                if sailor_available["display name"] == boat["display name"]:
                    sailor_available[event_date] = ""
                    break
            break


    sailors_available_file = open(sailors_available_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_available_file, fieldnames=available_field_names)
    writer.writeheader()
    for sailor in sailors_available:
        writer.writerow(sailor)
    sailors_available_file.close()

    return

def sailor_available(display_name, event_date):

    # Return True unless the sailor is a boat owner and the boat is scheduled on the event date.

    # Open the boat data and boat availability files.

    boats_data_filename = Working_directory + s_line_1.split(': ')[1].split(' //')[0]
    boats_data = [] # List of boat names.
    with open(boats_data_filename, mode='r') as boats_data_file:
        for boat in csv.DictReader(boats_data_file):
            boats_data.append(boat)

    boats_available_filename = Working_directory + s_line_3.split(': ')[1].split(' //')[0]
    boats_available = [] # List of boat names.
    with open(boats_available_filename, mode='r') as boats_available_file:
        for boat in csv.DictReader(boats_available_file):
            boats_available.append(boat)

    # Check whether the sailor identified by the display name is a boat owner
    # and (if so) is their boat sailing on the event date.
    # If it is, then the sailor is NOT available.

    for boat in boats_data:
        if boat["display name"] == display_name:
            for boat_available in boats_available:
                if boat_available["boat name"] == boat["boat name"]:
                    if boat_available[event_date] == "Y":
                        return False
    return True

def enrol_boat(form):

    # Add the boat described by the form to the boats data file, the boats available file
    # and the sailor whitelists.

    # Make the boats_data, sailors_data and boats_available lists from file.

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

    boats_available_filename = Working_directory + s_line_3.split(': ')[1].split(' //')[0]
    boats_available = [] # List of boat names.
    with open(boats_available_filename, mode='r') as boats_available_file:
        for boat in csv.DictReader(boats_available_file):
            boats_available.append(boat)

    # Compile the field names for each CSV file.

    boat_field_names = boats_data[0].keys()
    sailor_field_names = sailors_data[0].keys()
    available_field_names = boats_available[0].keys()

    # Process new boat data from the form.

    boat_name = canonicalize(single_line_from_form(form, "Boat name: "))
    owner_first_name = canonicalize(single_line_from_form(form, "Owner's first name: "))
    owner_last_name = canonicalize(single_line_from_form(form, "Owner's last name: "))
    email_address = canonicalize(single_line_from_form(form, "Email: "))
    mobile_number = canonicalize(single_line_from_form(form, "Mobile number: "))
    min_occupancy = single_line_from_form(form, "Minimum number of sailors assigned by the program: ")
    max_occupancy = single_line_from_form(form, "Maximum number of sailors assigned by the program: ")

    owner_display_name = owner_first_name + " " + owner_last_name[0]

    if single_line_from_form(form, "experienced sailor in the crew: ") == "Checked":
        request_assist = "True"
    else:
        request_assist = "False"

    # If an entry for the boat already exists, remove it from boats data and boats available lists and
    # delete it from each sailor's whitelist.

    for boat in boats_data:
        if boat["boat name"] == boat_name:
            boats_data.remove(boat)
    for boat in boats_available:
        if boat["boat name"] == boat_name:
            boats_available.remove(boat)

    for sailor in sailors_data:
        whitelist = sailor["whitelist"].replace(";" + boat_name, "")
        whitelist = whitelist.replace(boat_name + ";", "")
        sailor["whitelist"] = whitelist

    new_boat = {}
    available_boat = {}

    # Ask the operator if the boat's skipper is female.
    # Then make a list of the new boat data.

    print()
    if input("Does " + boat_name + " have a female skipper? (Y or return): ") == "Y":
        new_boat["female"] = "True"
    else:
        new_boat["female"] = "False"

    new_boat["boat name"] = boat_name
    new_boat["owner display name"] = owner_display_name
    new_boat["owner email address"] = email_address
    new_boat["mobile"] = mobile_number
    new_boat["min_occupancy"] = min_occupancy
    new_boat["max_occupancy"] = max_occupancy
    new_boat["request assist"] = request_assist

    # Add the new boat to the boats data file and boats available file.

    boats_data.append(new_boat)
    available_boat["boat name"] = boat_name
    boats_available.append(available_boat)

    # If the new boat has a female skipper, add it to the whitelist of every sailor that requested a female skipper.
    # If the new boat's skipper is not female, add it to every sailor's whitelist.

    if new_boat["female"] == "True":
        for sailor in sailors_data:
            if sailor["request female"] == "True":
                if len(sailor["whitelist"]) != 0:
                    sailor["whitelist"] += ";"
                sailor["whitelist"] += boat_name
    else:
        for sailor in sailors_data:
            if len(sailor["whitelist"]) != 0:
                sailor["whitelist"] += ";"
            sailor["whitelist"] += boat_name

    # Update the boats data, boats available and sailors data files.

    boats_data_file = open(boats_data_filename, 'w', newline='')
    writer = csv.DictWriter(boats_data_file, fieldnames=boat_field_names)
    writer.writeheader()
    for boat in boats_data:
        writer.writerow(boat)
    boats_data_file.close()

    boats_available_file = open(boats_available_filename, 'w', newline='')
    writer = csv.DictWriter(boats_available_file, fieldnames=available_field_names)
    writer.writeheader()
    for boat in boats_available:
        writer.writerow(boat)
    boats_available_file.close()

    sailors_data_file = open(sailors_data_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_data_file, fieldnames=sailor_field_names)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow(sailor)
    sailors_data_file.close()

    return


def enrol_sailor(form):

    # Add the sailor described by the form to the sailors data file, the sailors available file
    # and the sailor histories.

    # Import the sailors data file, the sailors history file and the sailors available file.

    sailors_data_filename = Working_directory + s_line_2.split(': ')[1].split(' //')[0]
    sailors_data = []  # list of sailor data dictionaries.
    with open(sailors_data_filename, mode='r') as sailors_data_file:
        for sailor in csv.DictReader(sailors_data_file):
            sailors_data.append(sailor)

    sailor_histories_filename = Working_directory + s_line_5.split(': ')[1].split(' //')[0]
    sailors_history = []  # list of sailor history dictionaries.
    with open(sailor_histories_filename, mode='r') as sailor_histories_file:
        for sailor in csv.DictReader(sailor_histories_file):
            sailors_history.append(sailor)

    sailors_available_filename = Working_directory + s_line_4.split(': ')[1].split(' //')[0]
    sailors_available = []  # list of sailor availability dictionaries.
    with open(sailors_available_filename, mode='r') as sailors_available_file:
        for sailor in csv.DictReader(sailors_available_file):
            sailors_available.append(sailor)

    # Compile the field names for each CSV file.

    sailor_field_names = sailors_data[0].keys()
    available_field_names = sailors_available[0].keys()
    history_field_names = sailors_history[0].keys()

    # Import the boats data file for use in the sailor's whitelist.

    boats_data_filename = Working_directory + s_line_1.split(': ')[1].split(' //')[0]
    boat_list = [] # List of boat dictionaries.
    with open(boats_data_filename, mode='r') as boats_data_file:
        for boat in csv.DictReader(boats_data_file):
            boat_list.append(boat)

    # Process the enrol sailor form data.

    first_name = canonicalize(single_line_from_form(form, "First name: "))
    last_name = canonicalize(single_line_from_form(form, "Last name: "))
    email_address = no_comma(single_line_from_form(form, "Email: "))
    membership_number = no_comma(single_line_from_form(form, "NSC membership number: "))
    background = single_line_from_form(form, "Background: ")
    experience = no_comma(no_new_line(multi_line_from_form(form, "experience: ")))

    display_name = first_name + " " + last_name[0]

    if membership_number == "":
        member = "False"
    else:
        member = "True"
    if single_line_from_form(form, "space allows: ") == "Checked":
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

    # If an entry for the sailor already exists, delete it from sailors data, sailors history and sailors availability.

    sailors_data = remove_dict(sailors_data, "display name", display_name)
    sailors_available = remove_dict(sailors_available, "display name", display_name)
    sailors_history = remove_dict(sailors_history, "display name", display_name)

    new_sailor = {}

    # Ask the user for the display name of the new sailor's partner.

    print()
    new_sailor["partner"] = input("Enter " + display_name + "'s partner display name: ")

    # If the sailor prefers a female skipper, add ALL boats to their whitelist.
    # Else only add boats whose skipper is not female.

    whitelist = ""
    if request_female == "True":
        for boat in boat_list:
            if len(whitelist) != 0:
                whitelist += ";"
            whitelist += boat["boat name"]
    else:
        for boat in boat_list:
            if not boat["female"] == "True":
                if len(whitelist) != 0:
                    whitelist += ";"
                whitelist += boat["boat name"]

    new_sailor["display name"] = display_name
    new_sailor["email address"] = email_address
    new_sailor["member"] = member
    new_sailor["skill"] = skill
    new_sailor["experience"] = experience
    new_sailor["request female"] = request_female
    new_sailor["whitelist"] = whitelist

    # Add the new sailor to sailors data and sailors available and sailor histories lists.

    sailors_data.append(new_sailor)

    available_sailor = {}
    available_sailor["display name"] = display_name
    for event_date in constants.event_dates:
        available_sailor[event_date] = ""
    sailors_available.append(available_sailor)

    sailor_history = {}
    sailor_history["display name"] = display_name
    for event_date in constants.event_dates:
        sailor_history[event_date] = ""
    sailors_history.append(sailor_history)

    # Update the sailors data, sailors available and sailors history files.

    sailors_data_file = open(sailors_data_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_data_file, fieldnames=sailor_field_names)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow(sailor)
    sailors_data_file.close()

    sailors_available_file = open(sailors_available_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_available_file, fieldnames=available_field_names)
    writer.writeheader()
    for sailor in sailors_available:
        writer.writerow(sailor)
    sailors_available_file.close()

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

    boat_name = single_line_from_form(form, "Boat name: ")

    # Update the boats availability file.

    for boat in boats_availability:
        if boat["boat name"] == boat_name:
            for event_date in constants.event_dates:
                if single_line_from_form(form, event_date + ": ") == "Register":
                    boat[event_date] = "Y"
                if single_line_from_form(form, event_date + ": ") == "Cancel":
                    boat[event_date] = ""
                sailor_unavailable(boat_name, event_date)

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

    available_field_names = sailors_availability[0].keys()

    first_name = canonicalize(single_line_from_form(form, "First name: "))
    last_name = canonicalize(single_line_from_form(form, "Last name: "))
    display_name = first_name.capitalize() + " " + last_name.capitalize()[0]

    for sailor in sailors_availability:
        if sailor["display name"] == display_name:
            for event_date in constants.event_dates:
                if single_line_from_form(form, event_date + ": ") == "Register":
                    if sailor_available(display_name, event_date):
                        sailor[event_date] = "Y"
                    else:
                        sailor[event_date] = ""
                elif single_line_from_form(form, event_date + ": ") == "Cancel":
                    sailor[event_date] = ""
                else: pass

    # Update the sailors availability file.

    sailors_availability_file = open(sailors_availability_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_availability_file, fieldnames=available_field_names)
    writer.writeheader()
    for sailor in sailors_availability:
        writer.writerow(sailor)
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

form_name = single_line_from_form(form, "Form name: ")

if form_name == "Enrol boat":
    enrol_boat(form)
elif form_name == "Enrol sailor":
    enrol_sailor(form)
elif form_name == "Register boat":
    register_boat(form)
    assignment.assignment()
elif form_name == "Register sailor":
    register_sailor(form)
    assignment.assignment()
else:
    raise Exception("Unrecognised form.")
