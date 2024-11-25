#!.venv/bin/python3.12

import database
import assignment
import prepare
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

def sailor_unavailable(boat_name, event_date):

    # If the owner of the boat is scheduled to be a sailor on the event date, then
    # sailing registration is cancelled.

    for boat in database.boats_data:
        if boat["boat name"] == boat_name:
            for sailor_availability in database.sailors_availability:
                if sailor_availability["display name"] == boat["display name"]:
                    sailor_availability[event_date] = ""
                    break
            break

    return

def sailor_availability(display_name, event_date):

    # Return True unless the sailor is a boat owner and the boat is scheduled on the event date.

    # Check whether the sailor identified by the display name is a boat owner
    # and (if so) is their boat sailing on the event date.
    # If it is, then the sailor is NOT available.

    for boat in database.boats_data:
        if boat["display name"] == display_name:
            for boat_availability in database.boats_availability:
                if boat_availability["boat name"] == boat["boat name"]:
                    if boat_availability[event_date] == "Y":
                        return False
    return True

def enrol_boat(form):

    # Add the boat described by the form to the boats data file, the boats available file
    # and the sailor whitelists.

    # Process new boat data from the form.

    boat_name = prepare.canonicalize(prepare.single_line_from_form(form, "Boat name: "))
    owner_first_name = prepare.canonicalize(prepare.single_line_from_form(form, "Owner's first name: "))
    owner_last_name = prepare.canonicalize(prepare.single_line_from_form(form, "Owner's last name: "))
    email_address = prepare.canonicalize(prepare.single_line_from_form(form, "Email: "))
    mobile_number = prepare.canonicalize(prepare.single_line_from_form(form, "Mobile number: "))
    min_occupancy = prepare.single_line_from_form(form, "Minimum number of sailors assigned by the program: ")
    max_occupancy = prepare.single_line_from_form(form, "Maximum number of sailors assigned by the program: ")

    owner_display_name = owner_first_name + " " + owner_last_name[0]

    if prepare.single_line_from_form(form, "experienced sailor in the crew: ") == "Checked":
        request_assist = "True"
    else:
        request_assist = "False"

    # If an entry for the boat already exists, remove it from boats data and boats availability lists and
    # delete it from each sailor's whitelist.

    for boat in database.boats_data:
        if prepare.standard(boat["boat name"]) == prepare.standard(boat_name):
            database.boats_data.remove(boat)

    for boat in database.boats_availability:
        if prepare.standard(boat["boat name"]) == prepare.standard(boat_name):
            database.boats_availability.remove(boat)

    for sailor in database.sailors_data:
        whitelist = sailor["whitelist"].replace(";" + boat_name, "")
        whitelist = whitelist.replace(boat_name + ";", "")
        sailor["whitelist"] = whitelist

    new_boat = {}
    available_boat = {}

    # Ask the operator if the boat's skipper is female.
    # Then make a list of the new boat data.

    print()
    user_input = input("Does " + boat_name + " have a female skipper? (Y/N): ")
    if user_input == "Y" or user_input == "y":
        new_boat["female"] = "True"
    else:
        new_boat["female"] = "False"

    new_boat["boat name"] = boat_name
    new_boat["display name"] = owner_display_name
    new_boat["owner email address"] = email_address
    new_boat["mobile"] = mobile_number
    new_boat["min occupancy"] = min_occupancy
    new_boat["max occupancy"] = max_occupancy
    new_boat["request assist"] = request_assist

    # Add the new boat to the boats data file and boats available file.

    database.boats_data.append(new_boat)

    available_boat = {}
    available_boat["boat name"] = boat_name
    for event_date in constants.event_dates:
        available_boat[event_date] = ""
    database.boats_availability.append(available_boat)

    # If the new boat has a female skipper, add it to the whitelist of every sailor that requested a female skipper.
    # If the new boat's skipper is not female, add it to every sailor's whitelist.

    if new_boat["female"] == "True":
        for sailor in database.sailors_data:
            if sailor["request female"] == "True":
                if len(sailor["whitelist"]) != 0:
                    sailor["whitelist"] += ";"
                sailor["whitelist"] += boat_name
    else:
        for sailor in database.sailors_data:
            if len(sailor["whitelist"]) != 0:
                sailor["whitelist"] += ";"
            sailor["whitelist"] += boat_name

    return


def enrol_sailor(form):

    # Add the sailor described by the form to the sailors data file, the sailors available file
    # and the sailor histories.

    # Process the enrol sailor form data.

    first_name = prepare.canonicalize(prepare.single_line_from_form(form, "First name: "))
    last_name = prepare.canonicalize(prepare.single_line_from_form(form, "Last name: "))
    email_address = prepare.no_comma(prepare.single_line_from_form(form, "Email: "))
    membership_number = prepare.number_from(prepare.single_line_from_form(form, "NSC membership number: "))
    background = prepare.single_line_from_form(form, "Background: ")
    experience = prepare.no_comma(prepare.no_new_line(prepare.multi_line_from_form(form, "experience: ")))

    display_name = prepare.unique_from(first_name, last_name, database.sailors_data)

    if membership_number == "":
        member = "False"
    else:
        member = "True"
    if prepare.single_line_from_form(form, "space allows: ") == "Checked":
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

    # If an entry for the sailor already exists, delete it from sailors data and sailors availability.
    # Don't remove from sailors history.

    for sailor in database.sailors_data:
        if sailor["display name"] == display_name:
            database.sailors_data.remove(sailor)

    for sailor in database.sailors_availability:
        if sailor["display name"] == display_name:
            database.sailors_availability.remove(sailor)

    new_sailor = {}

    # Ask the user for the display name of the new sailor's partner.

    print()
    new_sailor["partner"] = input("Enter " + display_name + "'s partner display name: ")

    # If the sailor prefers a female skipper, add ALL boats to their whitelist.
    # Else only add boats whose skipper is not female.

    whitelist = ""
    if request_female == "True":
        for boat in database.boats_data:
            if len(whitelist) != 0:
                whitelist += ";"
            whitelist += boat["boat name"]
    else:
        for boat in database.boats_data:
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

    # Add the new sailor to sailors data and sailors availability.

    database.sailors_data.append(new_sailor)

    available_sailor = {}
    available_sailor["display name"] = display_name
    for event_date in constants.event_dates:
        available_sailor[event_date] = ""
    database.sailors_availability.append(available_sailor)

    # If the sailor is already in the histories database, delete future event entries.
    # Otherwise, add the sailor to the histories database and set all events to empty.

    date_format = '%a %b %d'

    for sailor_history in database.sailor_histories:
        if sailor_history["display name"] == display_name:
            for event_date in constants.event_dates:
                if datetime.datetime.strptime(event_date, date_format) >= datetime.datetime.now():
                    sailor_history[event_date] = ""
            return

    sailor_history = {}
    sailor_history["display name"] = display_name
    for event_date in constants.event_dates:
        sailor_history[event_date] = ""
    database.sailor_histories.append(sailor_history)

    return


def register_boat(form):

    # Update the boats availability file with the information in the form.

    boat_name = prepare.single_line_from_form(form, "Boat name: ")

    # Update the boats availability file.

    for boat in database.boats_availability:
        if prepare.standard(boat["boat name"]) == prepare.standard(boat_name):
            for event_date in constants.event_dates:
                if prepare.single_line_from_form(form, event_date + ": ") == "Register":
                    boat[event_date] = "Y"
                if prepare.single_line_from_form(form, event_date + ": ") == "Cancel":
                    boat[event_date] = ""
                sailor_unavailable(boat_name, event_date)
            assignment.assignment()
            return
    raise Exception("The boat is not enrolled.")
    return


def register_sailor(form):

    # Check if the sailor is enrolled, based on entries in the sailor availability file.
    # In the event that the sailor IS enrolled, update the sailor availability file with
    # information from the form.
    # Check if the sailor is also a boat owner who is registered for any of the dates.
    #

    first_name = prepare.canonicalize(prepare.single_line_from_form(form, "First name: "))
    last_name = prepare.canonicalize(prepare.single_line_from_form(form, "Last name: "))
    display_name = prepare.unique_from(first_name, last_name, database.sailors_data)

    for sailor in database.sailors_availability:
        if sailor["display name"] == display_name:
            for event_date in constants.event_dates:
                if prepare.single_line_from_form(form, event_date + ": ") == "Register":
                    if sailor_availability(display_name, event_date):
                        sailor[event_date] = "Y"
                    else:
                        sailor[event_date] = ""
                elif prepare.single_line_from_form(form, event_date + ": ") == "Cancel":
                    sailor[event_date] = ""
                else: pass
            assignment.assignment()
            return
        else: pass
    print("The sailor is not enrolled.")
    for sailor in database.enrolments_pending:
        if sailor["display name"] == display_name: # There is an existing enrolments_pending entry.
            for event_date in constants.event_dates:
                if prepare.single_line_from_form(form, event_date + ": ") == "Register":
                    if sailor_availability(display_name, event_date):
                        sailor[event_date] = "Y"
                    else:
                        sailor[event_date] = ""
                elif prepare.single_line_from_form(form, event_date + ": ") == "Cancel":
                    sailor[event_date] = ""
                else: pass
            return
        else: pass
    new_sailor = {} # There is no existing enrolments_pending entry.
    new_sailor["display name"] = display_name
    for event_date in constants.event_dates:
        if prepare.single_line_from_form(form, event_date + ": ") == "Register":
            if sailor_availability(display_name, event_date):
                new_sailor[event_date] = "Y"
            else:
                new_sailor[event_date] = ""
        else: pass
    database.enrolments_pending.append(new_sailor)
    return

# --------------------------------------------------

database.begin()
crew_html.begin()

form_name = prepare.single_line_from_form(database.form, "Form name: ")

if form_name == "Enrol boat":
    enrol_boat(database.form)
elif form_name == "Enrol sailor":
    enrol_sailor(database.form)
elif form_name == "Register boat":
    register_boat(database.form)
elif form_name == "Register sailor":
    register_sailor(database.form)
else:
    raise Exception("Unrecognised form.")

database.end()
