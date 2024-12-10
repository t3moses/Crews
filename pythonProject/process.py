#!.venv/bin/python3.12

import database
import assignment
import strings
import crew_html
import constants
import datetime

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

def sailor_unavailable(boat_key, event_date):

    # If the owner of the boat is scheduled to be a sailor on the event date, then
    # their availability for sailing is cancelled.

    for boat in database.boats_data:
        if boat["key"] == boat_key:
            for sailor_availability in database.sailors_availability:
                if sailor_availability["key"] == boat["owner key"]:
                    sailor_availability[event_date] = ""
                    break
            break
    return

def sailor_availability(sailor_key, event_date):

    # Return True unless the sailor is a boat owner and the boat is scheduled on the event date.

    # Check whether the sailor identified by the sailor key is a boat owner
    # and (if so) is their boat sailing on the event date.
    # If it is, then the sailor is NOT available.

    for boat in database.boats_data:
        if boat["owner key"] == sailor_key:
            for boat_availability in database.boats_availability:
                if boat_availability["key"] == boat["key"]:
                    if boat_availability[event_date] == "Y":
                        return False
    return True

def remove_duplicate_boats(boat_key, boats_data, boats_availability, sailors_data):

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
    for event_date in constants.event_dates:
        available_boat[event_date] = ""
    boats_availability.append(available_boat)

    # If the new boat has a female skipper, add it to the whitelist of every sailor that requested a female skipper.
    # If the new boat's skipper is not female, add it to every sailor's whitelist.

    if new_boat["female"] == "True":
        for sailor in sailors_data:
            if sailor["request female"] == "True":
                if len(sailor["whitelist"]) != 0:
                    sailor["whitelist"] += ";"
                sailor["whitelist"] += new_boat["key"]
    else:
        for sailor in database.sailors_data:
            if len(sailor["whitelist"]) != 0:
                sailor["whitelist"] += ";"
            sailor["whitelist"] += new_boat["key"]
    return

def enrol_boat(form):

    # Add the boat described by the form to the boats data file, the boats available file
    # and the sailor whitelists.

    # Process new boat data from the form.

    boat_name = strings.single_line_from(form, "Boat name:")
    owner_first_name = strings.single_line_from(form, "Owner's first name:")
    owner_last_name = strings.single_line_from(form, "Owner's last name:")
    email_address = strings.single_line_from(form, "Owner's email address:")
    mobile_number = strings.single_line_from(form, "Owner's mobile number:")
    min_occupancy = strings.single_line_from(form, "Minimum number of sailors assigned by the program:")
    max_occupancy = strings.single_line_from(form, "Maximum number of sailors assigned by the program:")

    boat_key = strings.key_from_string(boat_name)
    owner_key = strings.key_from_strings(owner_first_name, owner_last_name)

    # If the boat account already exists, get the display name from the account.
    # Then remove the account from the boats database.
    # If the boat account does not exist, create the display name from the supplied boat name.

    if strings.key_exists(boat_key, database.boats_data):

        boats_data_copy = []
        for boat in database.boats_data:
            if boat["key"] == boat_key:
                display_name = boat["display name"]
            else:
                boats_data_copy.append(boat)
        database.boats_data = boats_data_copy

        boats_availability_copy = []
        for boat in database.boats_availability:
            if not boat["key"] == boat_key:
                boats_availability_copy.append(boat)
        database.boats_availability = boats_availability_copy

    else:
        display_name = strings.display_name_from_string(boat_name, database.boats_data)

    if strings.single_line_from(form, "experienced sailor in the crew:") == "Checked":
        assistance = "True"
    else:
        assistance = "False"

    new_boat = {}

    # Ask the operator if the boat's skipper is female.  Then make a list of the new boat data.

    print()
    user_input = input("Does " + boat_name + " have a female skipper? (Y/N):")
    if user_input == "Y" or user_input == "y":
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
    # Make the owner unavailable as a sailor on those dates.

    for boat in database.boats_availability:
        if boat["key"] == boat_key:
            for event_date in constants.event_dates:
                if strings.single_line_from(form, event_date + ":") == "Available":
                    boat[event_date] = "Y"
                else:
                    boat[event_date] = ""
                sailor_unavailable(boat_key, event_date)

    return


def enrol_sailor(form):

    display_name = ""

    # Add the sailor described by the form to the sailors data file, the sailors available file
    # and the sailor histories.

    first_name = strings.single_line_from(form, "First name:")
    last_name = strings.single_line_from(form, "Last name:")
    email_address = strings.single_line_from(form, "Email address:")
    membership_number = strings.number_from(strings.single_line_from(form, "NSC membership number:"))
    background = strings.single_line_from(form, "Background:")
    experience = strings.csv_safe(strings.multi_line_from(form, "Qualifications and experience:"))

    key = strings.key_from_strings(first_name, last_name)

    if membership_number == "":
        member = "False" # string not Boolean.
    else:
        member = "True"

    if strings.single_line_from(form, "space allows:") == "Checked":
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
    if request_female == "True":
        for boat in database.boats_data:
            if len(whitelist) != 0:
                whitelist += ";"
            whitelist += boat["key"]
    else:
        for boat in database.boats_data:
            if not boat["female"] == "True":
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
    # unless the sailor is available as an owner on those dates.

    available_sailor = {}
    available_sailor["key"] = key
    for event_date in constants.event_dates:
        if strings.single_line_from(form, event_date + ":") == "Available":
            if sailor_availability(display_name, event_date):
                available_sailor[event_date] = "Y"
            else:  # The sailor is scheduled as a boat owner.
                available_sailor[event_date] = ""
        else:
            available_sailor[event_date] = ""
    database.sailors_availability.append(available_sailor)

    """
    for sailor in database.sailors_availability:
        if sailor["key"] == key:
            for event_date in constants.event_dates:
                if strings.single_line_from(form, event_date + ":") == "I am available":
                    if sailor_availability(display_name, event_date):
                        sailor[event_date] = "Y"
                    else:  # The sailor is scheduled as a boat owner.
                        sailor[event_date] = ""
                else:
                    sailor[event_date] = ""
            return
        else:
            pass
    """

    # If the sailor is already in the histories database, delete future event entries.
    # Otherwise, add the sailor to the histories database and set all events to empty.

    date_format = '%a %b %d'

    for sailor_history in database.sailor_histories:
        if sailor_history["key"] == key:
            for event_date in constants.event_dates:
                if datetime.datetime.strptime(event_date, date_format) >= datetime.datetime.now():
                    sailor_history[event_date] = ""
            return

    sailor_history = {}
    sailor_history["key"] = key
    for event_date in constants.event_dates:
        sailor_history[event_date] = ""
    database.sailor_histories.append(sailor_history)

    return


def register_boat(form):

    # Update the boats availability file with the information in the form.

    boat_name = strings.single_line_from(form, "Boat name:")
    key = strings.key_from_string(boat_name)

    # If the boat account does not exist, use the default boat to create a new account.

    if not strings.key_exists(key, database.boats_data):
        display_name = strings.display_name_from_string(boat_name)
        new_boat = constants.default_boat
        new_boat["key"] = key
        new_boat["display name"] = display_name

        # Add the new boat to the boats database.

        database_from_boat(new_boat, database.boats_data, database.boats_availability, database.sailors_data)

    # Update the boats availability file.

    for boat in database.boats_availability:
        if boat["key"] == key:
            for event_date in constants.event_dates:
                if strings.single_line_from(form, event_date + ":") == "Available":
                    boat[event_date] = "Y"
                sailor_unavailable(key, event_date)
            return

    return


def register_sailor(form):

    # Check if the sailor is already enrolled, based on entries in the sailors data file.
    # If not, enrol the default sailor augmented with the name from the form.
    # Update the sailor availability file with information from the form.

    # Check if the sailor is also a boat owner who is registered for any of the dates.
    # Prioritize the boat owner role over the sailor role.

    first_name = strings.single_line_from(form, "First name:")
    last_name = strings.single_line_from(form, "Last name:")
    key = strings.key_from_strings(first_name, last_name)
    display_name = strings.display_name_from_strings(first_name, last_name, database.sailors_data)

    if not strings.key_exists(key, database.sailors_data):

        new_sailor = constants.default_sailor
        new_sailor["key"] = key
        new_sailor["display name"] = display_name

    for sailor in database.sailors_availability:
        if sailor["key"] == key:
            for event_date in constants.event_dates:
                if strings.single_line_from(form, event_date + ":") == "I am available":
                    if sailor_availability(display_name, event_date):
                        sailor[event_date] = "Y"
                    else: # The sailor is scheduled as a boat owner.
                        sailor[event_date] = ""
                else:
                    sailor[event_date] = ""
            return
        else: pass
    return

# --------------------------------------------------

database.begin()
crew_html.begin()

form_text = strings.text_from_string(database.form)

if form_text.count("open boat account"):
    enrol_boat(form_text)
elif form_text.count("open sailor account"):
    enrol_sailor(form_text)
elif form_text.count("enter boat availability"):
    register_boat(form_text)
elif form_text.count("enter sailor availability"):
    register_sailor(form_text)
else:
    raise Exception("Unrecognised form.")

assignment.assignment()

database.end()
