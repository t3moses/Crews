#!.venv/bin/python3.12

import sys
import database
import assignment
import strings
import crew_html
import constants
import datetime

def remove_duplicate_boats(boat_key, boats_data, boats_availability, sailors_data):

    # Remove the boat identified by boat_key from the database.

    for boat in boats_data:
        if boat_key == boat["key"]:
            boats_data.remove(boat)

    for boat in boats_availability:
        if boat_key == boat["key"]:
            boats_availability.remove(boat)

    for sailor in sailors_data:
        whitelist = sailor["whitelist"].replace(";" + boat_key, "")
        whitelist = whitelist.replace(boat_key + ";", "")
        sailor["whitelist"] = whitelist

    return

def database_from_boat(new_boat, boats_data, boats_availability, sailors_data):

    # Add the new boat to the database.

    boats_data.append(new_boat)

    available_boat = {}
    available_boat["key"] = new_boat["key"]
    for event_id in constants.event_ids:
        available_boat[event_id] = ""
    boats_availability.append(available_boat)

    # If the new boat has a female skipper, add it to the whitelist of every sailor that requested a female skipper.
    # If the new boat's skipper is not female, add it to every sailor's whitelist.

    if new_boat["female"].upper() == "TRUE":
        for sailor in sailors_data:
            if sailor["request female"].upper() == "TRUE":
                if len(sailor["whitelist"]) != 0:
                    sailor["whitelist"] += ";"
                sailor["whitelist"] += new_boat["key"]
    else:
        for sailor in database.sailors_data:
            if len(sailor["whitelist"]) != 0:
                sailor["whitelist"] += ";"
            sailor["whitelist"] += new_boat["key"]
    return

def user_input_from_form(form):

    boundary = {}  # dictionary containing the start and end indices of one field.
    boundaries = []  # list of boundaries.
    form_len = len(form)
    form_name_start = int
    form_name_end = int
    sequence = "0ae2808a0a"
    seq_len = 3
    state = 0
    for i in range(form_len):
        match state:
            case 0:
                if i + seq_len > form_len:
                    state = 4  # reached end of form.
                elif form[i:i + seq_len].encode().hex() == sequence: # Start of form name.
                    form_name_start = i + seq_len
                    sequence = "0a0a"
                    seq_len = 2
                    state = 1
                else:
                    state = 0  # no state change.
            case 1:
                if i + seq_len > form_len:
                    state = 4  # reached end of form.
                elif form[i:i + seq_len].encode().hex() == sequence: # End of form name.
                    form_name_end = i
                    sequence = "3a0a"
                    seq_len = 2
                    state = 2
                else:
                    state = 1  # no state change.
            case 2:
                if i + seq_len > form_len:
                    state = 4  # reached end of form.
                elif form[i:i + seq_len].encode().hex() == sequence:
                    boundary["start"] = i + seq_len # Start of first field.
                    sequence = "c2a0c2a00a"
                    seq_len = 3
                    state = 3
                else: state = 2  # no state change.
            case 3:
                if i + seq_len > form_len:
                    state = 4  # reached end of form.
                elif form[i:i + seq_len].encode().hex() == sequence:
                    boundary["end"] = i # End of field.
                    boundaries.append(boundary.copy())
                    boundary["start"] = i + seq_len # Start of next field.
                    state = 3  # no state change.
                else:
                    state = 3  # no state change.
            case _:
                continue

    # Make the user input dictionary.

    user_input = {}
    key = "Form name"
    value = strings.csv_safe(form[form_name_start: form_name_end])
    user_input.update({key: value})

    for boundary in boundaries:
        key_value = form[boundary["start"] : boundary["end"]].partition(":\n")
        key = key_value[0]
        value = strings.csv_safe(key_value[2])
        user_input.update({key: value})

    return user_input

def enrol_boat(user_input):

    # Add the boat described by the form to the boats data file, the boats available file
    # and the sailor whitelists.

    # Process new boat data from the form.

    boat_name = user_input.get("Boat name")
    owner_first_name = user_input.get("Owner's first name")
    owner_last_name = user_input.get("Owner's last name")
    email_address = user_input.get("Owner's email address")
    mobile_number = user_input.get("Owner's mobile number")
    if mobile_number == None: # mobile number is not a required field in the web form.
        mobile_number = "None"
    min_occupancy = user_input.get("Minimum number of sailors assigned by the program")
    max_occupancy = user_input.get("Maximum number of sailors assigned by the program")

    boat_key = strings.key_from_string(boat_name)
    owner_key = strings.key_from_strings(owner_first_name, owner_last_name)

    # If the boat account already exists, get the display name from the account.
    # Then remove the account from the boats database and from the sailor whitelists.
    # If the boat account does not exist, create the display name from the supplied boat name.

    if strings.key_exists(boat_key, database.boats_data):

        for boat in database.boats_data:
            if boat["key"] == boat_key:
                display_name = boat["display name"]

        remove_duplicate_boats(boat_key, database.boats_data, database.boats_availability, database.sailors_data)

    else:
        display_name = strings.display_name_from_string(boat_name)

    if user_input.get("Include an experienced sailor in the crew") == "Checked":
        assistance = "True"
    else:
        assistance = "False"

    new_boat = {}

    # Ask the operator if the boat's skipper is female.  Then make a list of the new boat data.

    print()
    response = input("Does " + boat_name + " have a female skipper? (Y/N):")
    if response.upper() == "Y":
        new_boat["female"] = "True"
    else:
        new_boat["female"] = "False"

    new_boat["key"] = boat_key
    new_boat["owner key"] = owner_key
    new_boat["display name"] = display_name
    new_boat["email address"] = email_address
    new_boat["mobile"] = mobile_number
    new_boat["min occupancy"] = min_occupancy
    new_boat["max occupancy"] = max_occupancy
    new_boat["assistance"] = assistance

    # Add the new boat to the boats database.

    database_from_boat(new_boat, database.boats_data, database.boats_availability, database.sailors_data)

    # Add the new boat availability to the boats availability database.

    for boat in database.boats_availability:
        if boat["key"] == boat_key:
            for event_id in constants.event_ids:
                if user_input.get(event_id) == "Available":
                    boat[event_id] = "Y"
                else:
                    boat[event_id] = ""

    return


def enrol_sailor(user_input):

    display_name = ""

    # Add the sailor described by the form to the sailors data file, the sailors available file
    # and the sailor histories file.

    first_name = user_input.get("First name")
    last_name = user_input.get("Last name")
    email_address = user_input.get("Email address")
    membership_number = user_input.get("NSC membership number")
    background = user_input.get("Background")
    experience = user_input.get("Qualifications and experience", "")

    key = strings.key_from_strings(first_name, last_name)

    if ( membership_number == None ) or ( len( membership_number ) < constants.min_membership_number_length ):
        member = "False" # member is a string not a Boolean.
    else:
        member = "True"

    if user_input.get("(Women only) I would like to sail with a female captain when space allows") == "Checked":
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

    # If an entry for the sailor already exists, remember its display name.  Then delete it from
    # sailors data and sailors availability.  Don't remove it from sailors history.

    if strings.key_exists(key, database.sailors_data):

        for sailor in database.sailors_data:
            if sailor["key"] == key:
                display_name = sailor["display name"]

        sailors_data_copy = []
        for sailor in database.sailors_data:
            if not sailor["key"] == key:
                sailors_data_copy.append(sailor)
        database.sailors_data = sailors_data_copy

        sailors_availability_copy = []
        for sailor in database.sailors_availability:
            if not sailor["key"] == key:
                sailors_availability_copy.append(sailor)
        database.sailors_availability = sailors_availability_copy

    else:
        display_name = strings.display_name_from_strings(first_name, last_name, database.sailors_data)

    new_sailor = {}

    # Ask the user for the display name of the new sailor's partner.

    print()
    partner_display_name = input("Enter " + display_name + "'s partner display name:")

    new_sailor["partner key"] = ""
    for sailor in database.sailors_data:
        if sailor["display name"] == partner_display_name:
            new_sailor["partner key"] = sailor["key"]
            break

    # If the sailor prefers a female skipper, add ALL boats to their whitelist.
    # Else only add boats whose skipper is not female.

    whitelist = ""
    if request_female.upper() == "TRUE":
        for boat in database.boats_data:
            if len(whitelist) != 0:
                whitelist += ";"
            whitelist += boat["key"]
    else:
        for boat in database.boats_data:
            if not boat["female"].upper() == "TRUE":
                if len(whitelist) != 0:
                    whitelist += ";"
                whitelist += boat["key"]

    new_sailor["key"] = key
    new_sailor["display name"] = display_name
    new_sailor["email address"] = email_address
    new_sailor["member"] = member
    new_sailor["skill"] = skill
    new_sailor["experience"] = experience
    new_sailor["request female"] = request_female
    new_sailor["whitelist"] = whitelist

    # Add the new sailor to sailors data and sailors availability.

    database.sailors_data.append(new_sailor)

    # Add the new sailor availability to the sailors availability database,

    available_sailor = {}
    available_sailor["key"] = key
    for event_id in constants.event_ids:
        if user_input.get(event_id) == "Available":
            available_sailor[event_id] = "A"
        else:
            available_sailor[event_id] = ""

    database.sailors_availability.append(available_sailor)

    # If the sailor is already in the histories database, delete future event entries,
    # leaving past availability untouched..
    # Otherwise, add the sailor to the histories database and set all events to empty.

    date_format = '%a %b %d'
    this_year = datetime.date.today().year
    today = datetime.date.today()

    if strings.key_exists(key, database.sailor_histories):
        for sailor_history in database.sailor_histories:
            if sailor_history["key"] == key:
                for event_id in constants.event_ids:
                    full_event_id = datetime.datetime.strptime(event_id, date_format).replace(year = this_year).date()
                    if full_event_id >= today:
                        sailor_history[event_id] = ""
    else:
        sailor_history = {}
        sailor_history["key"] = key
        for event_id in constants.event_ids:
            sailor_history[event_id] = ""
        database.sailor_histories.append(sailor_history)

    return


def register_boat(user_input):

    # Update the boats availability file with the information in the form.

    boat_name = user_input.get("Boat name")
    key = strings.key_from_string(boat_name)

    # If the boat account does not exist, create and populate a new account using the default boat data.

    if strings.key_exists(key, database.boats_data):
        pass
    else:
        display_name = strings.display_name_from_string(boat_name)
        new_boat = constants.default_boat
        new_boat["key"] = key
        new_boat["display name"] = display_name
        database_from_boat(new_boat, database.boats_data, database.boats_availability, database.sailors_data)

    # Update the boats availability file.

    date_format = '%a %b %d'
    this_year = datetime.date.today().year
    today = datetime.date.today()

    for boat in database.boats_availability:
        if boat["key"] == key:
            for event_id in constants.event_ids:
                full_event_id = datetime.datetime.strptime(event_id, date_format).replace(year = this_year).date()
                if full_event_id >= today:
                    if user_input.get(event_id) == "Register":
                        boat[event_id] = "Y"
                    elif user_input.get(event_id) == "Cancel":
                        boat[event_id] = ""
                    else:
                        pass


def register_sailor(user_input):

    # Get the sailor data from the user input.

    first_name = user_input.get("First name")
    last_name = user_input.get("Last name")
    key = strings.key_from_strings(first_name, last_name)
    display_name = strings.display_name_from_strings(first_name, last_name, database.sailors_data)

    # Check if the sailor is already enrolled, based on entries in the sailors data,
    # sailors availability and sailor histories files.

    # If they are not already enrolled, create and populate entries in the respective files.

    if strings.key_exists(key, database.sailors_data):
        pass
    else:
        new_sailor = constants.default_sailor
        new_sailor["key"] = key
        new_sailor["display name"] = display_name
        whitelist = ""
        for boat in database.boats_data:
            if boat["female"].upper() == "FALSE":
                whitelist += boat["key"] + ";"
        whitelist = whitelist.rstrip(";")
        new_sailor["whitelist"] = whitelist
        database.sailors_data.append(new_sailor)

    if strings.key_exists(key, database.sailors_availability):
        pass
    else:
        available_sailor = {}
        available_sailor["key"] = key
        for event_id in constants.event_ids:
            available_sailor[event_id] = ""
        database.sailors_availability.append(available_sailor)

    if strings.key_exists(key, database.sailor_histories):
        pass
    else:
        sailor_history = {}
        sailor_history["key"] = key
        for event_id in constants.event_ids:
            sailor_history[event_id] = ""
        database.sailor_histories.append(sailor_history)

    # Update the sailor's future availability in the sailors availability database, based on user input,

    date_format = '%a %b %d'
    this_year = datetime.date.today().year
    today = datetime.date.today()

    for available_sailor in database.sailors_availability:
        if available_sailor["key"] == key:
            for event_id in constants.event_ids:
                full_event_id = datetime.datetime.strptime(event_id, date_format).replace(year = this_year).date()
                if full_event_id >= today:
                    if user_input.get(event_id) == "Register":
                        available_sailor[event_id] = "A"
                    elif user_input.get(event_id) == "Cancel":
                        available_sailor[event_id] = ""
                    else:
                        pass

# --------------------------------------------------

database.begin()
crew_html.begin()

# Add the form contents to the database.

user_input = user_input_from_form(database.form)

if user_input.get("Form name") == "Open boat account": enrol_boat(user_input)
elif user_input.get("Form name") == "Open sailor account": enrol_sailor(user_input)
elif user_input.get("Form name") == "Enter boat availability": register_boat(user_input)
elif user_input.get("Form name") == "Enter sailor availability": register_sailor(user_input)
else:
    print("Unrecognised form.")
    sys.exit(1)

assignment.assignment()

database.end()
