
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

def standard(name):

    # Remove leading and trailing spaces.
    # Convert the input to lower case.

    standardd_name = ""
    for i in range(len(name)):
        if name[i] == " " or name[i] == "-":
            pass
        else:
            standardd_name += name[i]

    standardd_name = standardd_name.strip().casefold()

    return standardd_name

def number_from( input ):

    # Returns the input string stripped of all alphas and punctuation.
    # If the input contains no digits, then it returns the empty string.

    number = ""
    for i in range(len(input)):
        if input[i].isdigit():
            number += input[i]
        else: pass
    return number


def unique_from( first, last, sailors_data ):

    # Returns a unique display name.

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
