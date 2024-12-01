
import constants
import csv

boats_data_filename = ""
sailors_data_filename = ""
boats_availability_filename = ""
sailors_availability_filename = ""
sailor_histories_filename = ""
enrolments_pending_filename = ""
user_input_form_filename = ""
assignments_file_name = ""

boats_data = [] # list of boat data dictionaries.
sailors_data = [] # list of sailor data dictionaries.
boats_availability = [] # list of boats availability dictionaries.
sailors_availability = [] # list of sailors availability dictionaries.
sailor_histories = [] # list of sailor histories dictionaries.
enrolments_pending = [] # list of enrolments that are pending.

form = "" # contents of the user input form.
html = "" # contents of the event calendar out[ut html.

upper_crew_size = 0 # Used to calculate html column width.

def begin():

    # Build the database from files.

    global boats_data_filename
    global sailors_data_filename
    global boats_availability_filename
    global sailors_availability_filename
    global sailor_histories_filename
    global enrolments_pending_filename
    global user_input_form_filename
    global assignments_file_name
    global boats_data
    global sailors_data
    global boats_availability
    global sailors_availability
    global sailor_histories
    global form
    global upper_crew_size

    Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/"

    with open(Working_directory + "Config/" + "config.txt", "r") as f_config:
        s_line_1 = f_config.readline()  # boats data
        s_line_2 = f_config.readline()  # sailors data
        s_line_3 = f_config.readline()  # boats availability
        s_line_4 = f_config.readline()  # sailors availability
        s_line_5 = f_config.readline()  # sailors history
        s_line_6 = f_config.readline()  # enrolments pending
        s_line_7 = f_config.readline()  # user input form
        s_line_8 = f_config.readline()  # events path

    boats_data_filename += Working_directory+s_line_1.split(': ')[1].split(' //')[0]
    sailors_data_filename = Working_directory+s_line_2.split(': ')[1].split(' //')[0]
    boats_availability_filename = Working_directory+s_line_3.split(': ')[1].split(' //')[0]
    sailors_availability_filename = Working_directory+s_line_4.split(': ')[1].split(' //')[0]
    sailor_histories_filename = Working_directory+s_line_5.split(': ')[1].split(' //')[0]
    enrolments_pending_filename = Working_directory+s_line_6.split(': ')[1].split(' //')[0]
    user_input_form_filename = Working_directory+s_line_7.split(': ')[1].split(' //')[0]
    assignments_file_name = Working_directory+s_line_8.split(': ')[1].split(' //')[0]

    # Open the boat data file.  If it doesn't yet exist, create it.
    # Import boats data.

    try:
        boats_data_file = open(boats_data_filename, 'r', newline='')
    except FileNotFoundError:
        print("Creating boats data file.")
        boat_header_row = constants.boat_header_row
        boats_data_file = open(boats_data_filename, 'w+', newline='')
        writer = csv.DictWriter(boats_data_file, fieldnames=boat_header_row)
        writer.writeheader()
    for boat in csv.DictReader(boats_data_file):
        boats_data.append(boat)
    boats_data_file.close()

    # Open the sailor data file.  If it doesn't yet exist, create it.
    # Import sailors data.

    try:
        sailors_data_file = open(sailors_data_filename, 'r', newline='')
    except FileNotFoundError:
        print("Creating sailors data file.")
        sailor_header_row = constants.sailor_header_row
        sailors_data_file = open(sailors_data_filename, 'w+', newline='')
        writer = csv.DictWriter(sailors_data_file, fieldnames=sailor_header_row)
        writer.writeheader()
    for sailor in csv.DictReader(sailors_data_file):
        sailors_data.append(sailor)
    sailors_data_file.close()

    # Open the boat availability file.  If it doesn't yet exist, create it.

    try:
        boats_availability_file = open(boats_availability_filename, 'r', newline='')
    except FileNotFoundError:
        print("Creating boats availability file.")
        boat_availability_header_row = ["key"] + constants.event_dates
        boats_availability_file = open(boats_availability_filename, 'w+', newline='')
        writer = csv.DictWriter(boats_availability_file, fieldnames=boat_availability_header_row)
        writer.writeheader()
    for availability in csv.DictReader(boats_availability_file):
        boats_availability.append(availability)
    boats_availability_file.close()

    # Open the sailor availability file.  If it doesn't yet exist, create it.

    try:
        sailors_availability_file = open(sailors_availability_filename, 'r', newline='')
    except FileNotFoundError:
        print("Creating sailors availability file.")
        sailor_availability_header_row = ["key"] + constants.event_dates
        sailors_availability_file = open(sailors_availability_filename, 'w+', newline='')
        writer = csv.DictWriter(sailors_availability_file, fieldnames=sailor_availability_header_row)
        writer.writeheader()
    for availability in csv.DictReader(sailors_availability_file):
        sailors_availability.append(availability)
    sailors_availability_file.close()

    # Open the sailor histories file.  If it doesn't yet exist, create it.

    try:
        sailor_histories_file = open(sailor_histories_filename, 'r', newline='')
    except FileNotFoundError:
        print("Creating sailor histories file.")
        sailor_histories_header_row = ["key"] + constants.event_dates
        sailor_histories_file = open(sailor_histories_filename, 'w+', newline='')
        writer = csv.DictWriter(sailor_histories_file, fieldnames=sailor_histories_header_row)
        writer.writeheader()
    for sailor in csv.DictReader(sailor_histories_file):
        sailor_histories.append(sailor)
    sailor_histories_file.close()

    # Confirm that boat names are consistent between the boats_availability and boat_data files.

    boats_from_availability = []
    for boat in boats_availability:
        boats_from_availability.append(boat["key"])
    boats_from_data = []
    for boat in boats_data:
        boats_from_data.append(boat["key"])
    if bool(set(boats_from_availability) ^ set(boats_from_data)): # difference
        raise Exception("Boat availability is inconsistent with boat data.")

    # Confirm that sailor names are consistent between the sailor_availability and sailor_data files.

    sailors_from_availability = []
    for sailor in sailors_availability:
        sailors_from_availability.append(sailor["key"])
    sailors_from_data = []
    for sailor in sailors_data:
        sailors_from_data.append(sailor["key"])
    if bool(set(sailors_from_availability) ^ set(sailors_from_data)):
        raise Exception("Sailor availability is inconsistent with sailor data.")

    # Confirm that sailor whitelists are consistent with boats_sata.

    boats_from_data = [""]
    for boat in boats_data:
        boats_from_data.append(boat["key"])
    for sailor in sailors_data:
        sailor_whitelist = sailor["whitelist"].split(";")
        if not bool(set(sailor_whitelist) <= set(boats_from_data)):
            raise Exception("Sailor whitelist is inconsistent with boat data.")

    # Import the user input form.

    form_file = open(user_input_form_filename, "r")
    form = form_file.read()
    form_file.close()

    # calculate the upper bound on the crew size.

    upper_crew_size = 1
    for boat in boats_data:
        upper_crew_size = max(upper_crew_size, int(boat["max occupancy"]))

    return

def end():

    # Update the boats data file.

    global boats_data_filename
    global sailors_data_filename
    global boats_availability_filename
    global sailors_availability_filename
    global sailor_histories_filename
    global enrolments_pending_filename
    global assignments_file_name
    global boats_data
    global sailors_data
    global boats_availability
    global sailors_availability
    global sailor_histories
    global enrolments_pending
    global html

    boats_data_file = open(boats_data_filename, 'w', newline='')
    writer = csv.DictWriter(boats_data_file, fieldnames=constants.boat_header_row)
    writer.writeheader()
    for boat in boats_data:
        writer.writerow(boat)
    boats_data_file.close()

    # Update the sailors data file.

    sailors_data_file = open(sailors_data_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_data_file, fieldnames=constants.sailor_header_row)
    writer.writeheader()
    for sailor in sailors_data:
        writer.writerow(sailor)
    sailors_data_file.close()

    # Update the boats availability file.

    boat_availability_header_row = ["key"] + constants.event_dates
    boats_availability_file = open(boats_availability_filename, 'w', newline='')
    writer = csv.DictWriter(boats_availability_file, fieldnames=boat_availability_header_row)
    writer.writeheader()
    for boat in boats_availability:
        writer.writerow(boat)
    boats_availability_file.close()

    # Update the sailors availability file.

    sailor_availability_header_row = ["key"] + constants.event_dates
    sailors_availability_file = open(sailors_availability_filename, 'w', newline='')
    writer = csv.DictWriter(sailors_availability_file, fieldnames=sailor_availability_header_row)
    writer.writeheader()
    for sailor in sailors_availability:
        writer.writerow(sailor)
    sailors_availability_file.close()

    # Update the sailor histories file.

    sailor_histories_header_row = ["key"] + constants.event_dates
    sailor_histories_file = open(sailor_histories_filename, 'w', newline='')
    writer = csv.DictWriter(sailor_histories_file, fieldnames=sailor_histories_header_row)
    writer.writeheader()
    for sailor_history in sailor_histories:
        writer.writerow(sailor_history)
    sailor_histories_file.close()

    assignments_file = open(assignments_file_name, 'w', newline='')
    assignments_file.write(html)
    assignments_file.close()

    return