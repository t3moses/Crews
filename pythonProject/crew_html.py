
import math
import database

top = ""
tail = ""
contents = ""
table_width = 0
column_width = 0

def begin():

    global top
    global tail
    global column_width

    # Set up the top and tail of the html file.

    top += "<!DOCTYPE html><html><head><style>"
    top += "table {font-family: arial, sans-serif;border-collapse: collapse;}"
    top += "td {border: 1px solid #dddddd;text-align: left;padding: 8px;}"
    top += "tr:nth-child(even) {background-color: #dddddd;}"
    top += "</style></head><body>"

    tail += "</body></html>"

    column_width = int( 100 / ( database.upper_crew_size + 1 ))

    return

def html(event):

    global column_width

    # Add the html table for one event to the document.

    max_crew_size = 0
    for crew in event["flotilla"]:
        crew_size = len(crew["sailors"])
        if crew_size > max_crew_size:
            max_crew_size = crew_size
    table_width = ( max_crew_size + 1 ) * column_width

    global contents
    contents += "<h2>Event date: " + event["date"] + "</h2>"
    contents += "<table width = " + str(table_width) + "%><th><tr>"
    for column in range(max_crew_size + 1):
        if column == 0:
            contents += "<td width = " + str(column_width) + "%>Boat</td>"
        elif column == 1:
            contents += "<td width = " + str(column_width) + "%>Crew</td>"
        else:
            contents += "<td width = " + str(column_width) + "%></td>"
    contents += "</tr></th>"
    for crew in event["flotilla"]:
        for boat in database.boats_data:
            if crew["boat"] == boat["key"]:
                contents += "<tr><td>" + boat["display name"] + "</td>"
                for event_sailor in crew["sailors"]:
                    for sailor in database.sailors_data:
                        if event_sailor == sailor["key"]:
                            contents += "<td>" + sailor["display name"] + "</td>"
                empty_cells = max_crew_size - len(crew["sailors"])
                for _ in range( empty_cells ):
                    contents += "<td>" + "" + "</td>"
                contents += "</tr>"

    for row_index in range(math.ceil(len(event["wait list"]) / max_crew_size)):
        if row_index == 0:
            # Add a blank line here.
            contents += "<tr>"
            for column in range(max_crew_size + 1):
                contents += "<td></td>"
            contents += "</tr>"
            contents += "<tr><td>Wait list</td>"
        else:
            contents += "<tr><td></td>"
        for column_index in range(max_crew_size):
            cell_index = max_crew_size * row_index + column_index
            if cell_index < len(event["wait list"]):
                wait_list_sailor_key = event["wait list"][cell_index]
                for sailor in database.sailors_data:
                    if wait_list_sailor_key == sailor["key"]:
                        contents += "<td>" + sailor["display name"] + "</td>"
            else:
                contents += "<td></td>"
    contents += "</tr></table>"

    html = top + contents + tail

    return html
