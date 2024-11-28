
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
    # Otherwise, return the contents of the form between the field name and the first : character,
    # except for the portion from the last new line (inclusive) to the end.

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

def standard(first, last):

    # Remove non-alpha characters and leading and trailing spaces.
    # Convert to lower case and concatenate first and last.

    standard_first = ""
    for char in first:
        if char.isalpha():
            standard_first += char
    standard_first = standard_first.strip().casefold()

    standard_last = ""
    for char in last:
        if char.isalpha():
            standard_last += char
    standard_last = standard_last.strip().casefold()

    return standard_first + standard_last

def number_from( input ):

    # Returns the input string stripped of all alphas and punctuation.
    # If the input contains no digits, then it returns the empty string.

    number = ""
    for i in range(len(input)):
        if input[i].isdigit():
            number += input[i]
        else: pass
    return number


def form_unique_from( first, last, sailors_data ):

    # Returns a name, derived from the first and last names, that does not already exist in the sailors data file.

    first_strip = first.strip().capitalize()
    last_strip = last.strip().capitalize()
    full = first_strip + " " + last_strip
    new_display_name = first_strip + " " + last_strip[0]

    full_len = len(full)
    for sailor in sailors_data:
        unique_len = len(new_display_name)
        for i in range(unique_len, full_len):
            if new_display_name == sailor["display name"]:
                new_display_name += full[i]
            else: break
    return new_display_name

def match_unique_from( first, last, sailors_data ):

    # Returns a display name, derived from the first and last names, that either matches
    # the most specific name in the sailors data file, or was not found in the file.

    first_strip = first.strip().capitalize()
    last_strip = last.strip().capitalize()
    full = first_strip + " " + last_strip
    match_display_name = full
    full_len = len( full )
    unique_len = len(first_strip + " " + last_strip[0])

    match_found = True
    for i in range(full_len, unique_len, -1):
        for sailor in sailors_data:
            if match_display_name == sailor["display name"]:
                match_found = True
                break
            else:
                match_found = False
        if match_found: break
        match_display_name = full[ :  -(full_len - i + 1 )]
    return match_display_name

def sailor_account_exists_for(first, last, sailors_data):

    # If a sailor with the supplied name already has an account, return True.
    # Otherwise, return False.

    standard_name = standard(first, last)
    for sailor in sailors_data:
        if standard_name == sailor["standard_name"]:
            return True
    return False


def boat_account_exists_for(boat_name, boats_data):

    # If a boat with the supplied name already has an account, return True.
    # Otherwise, return False.

    for boat in boats_data:
        if boat_name == boat["boat_name"]:
            return True
    return False


def unique_display_name_from(full_name, sailors_data):
    
    return
