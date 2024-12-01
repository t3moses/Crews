
def single_line_from(form, field_name):

    # Return the value of the named field from the form.
    # If the named field is not present in the form, return an empty string.
    # Otherwise, return the contents of the form between the field name and the end of the line.

    if form.find(field_name) == -1:
        return ""
    else:
        return (form.rpartition(field_name + "\n")[2]).partition("\n")[0]

def multi_line_from(form, field_name):

    # Return the value of the named field from the form.
    # If the named field is not present in the form, return an empty string.
    # Otherwise, return the contents of the form between the field name and the first : character,
    # except for the portion from the last new line (inclusive) to the end.

    if form.find(field_name) == -1:
        return ""
    else:
        new_field = form.rpartition(field_name + "\n")[2].rpartition(":")[0]
        new_field = new_field.rpartition("\n")[0]
        return new_field


def csv_safe( string ):

    safe_string = ""
    for char in string:
        if char == ",":
            safe_string += "&#44;"
        elif ord(char) == 10: # new line.
            safe_string += "&#10;"
        else:
            safe_string += char
    return safe_string

def text_from_string(string):

    text_string = ""
    for char in string:
        if (char.isascii() and char.isprintable()) or char == "\n":
            text_string += char
    return text_string

def key_from_string(name):

    # Return a key from the supplied name, stripped of all non-alpha characters.

    key = ""
    for char in name:
        if char.isalpha() or char.isdigit():
            key += char
    return key.casefold()

def key_from_strings(first, last):

    # Return a key from the supplied first and last names.

    key_first = key_from_string(first)
    key_last = key_from_string(last)
    return key_first + key_last


def number_from( input ):

    # Returns the input string stripped of all alphas and punctuation.
    # If the input contains no digits, then it returns the empty string.

    number = ""
    for i in range(len(input)):
        if input[i].isdigit():
            number += input[i]
        else: pass
    return number

def display_name_from_string( name, database ):

    # Returns a display name, derived from the supplied name,
    # that does not already exist in the database.

    display_name = name
    return display_name

def display_name_from_strings( first, last, database ):

    # Returns a display name, derived from the supplied first and last names,
    # that does not already exist in the database.

    display_name = first.capitalize()
    last = last.capitalize()

    for i in range(len(last)):
        display_name += last[i]
        if not display_name_exists(display_name, database):
            break
    return display_name

def display_name_exists(display_name, database):

    # If a boat with the supplied key name already has an account, return True.
    # Otherwise, return False.

    for record in database:
        if display_name == record["display name"]:
            return True
    return False

def key_exists(key, database):

    # If a boat with the supplied key name already has an account, return True.
    # Otherwise, return False.

    for record in database:
        if key == record["key"]:
            return True
    return False

