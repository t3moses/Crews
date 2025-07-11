
import database
import strings

top = ""
tail = ""

def begin():

    global top
    global tail

    # Set up the top and tail of the html file.

    top += "<!DOCTYPE html><html><head><style>"
    top += "table {font-family: arial, sans-serif; font-size: 40px; border-collapse: collapse;}"
    top += "td {border: 20px solid #999999;text-align: left; padding: 8px;}"
#    top += "tr:nth-child(even) {background-color: #dddddd;}"
    top += "</style></head><body>"

    tail += "</body></html>"

    return



def html(event):

    contents = "<table>"

    for crew in event["flotilla"]:

        number_of_tickets = [int(boat["max occupancy"]) for boat in database.boats_data if crew["boat"] == boat["key"]][0]
        boat_display_name = [boat["display name"] for boat in database.boats_data if crew["boat"] == boat["key"]][0]
        for _ in range(number_of_tickets):
            contents += "<tr>"
            contents += "<td> + </td>"
            contents += "<td>" + event["date"] + "</td>"
            contents += "<td>" + boat_display_name + "</td>"
            contents += "</tr>"

    contents += "</table>"

    return top + contents + tail
