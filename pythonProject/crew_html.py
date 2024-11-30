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

def html(scored_crews, wait_list, event_date):

    global column_width

    # Add the html table for one event to the document.

    crews = scored_crews["crews"]
    crews_score = scored_crews["crews score"]

    max_crew_size = 0
    for crew in crews:
        crew_size = len(crew["sailors"])
        if crew_size > max_crew_size:
            max_crew_size = crew_size
    crew_size = len(wait_list)
    if crew_size > max_crew_size:
        max_crew_size = crew_size

    table_width = ( max_crew_size + 1 ) * column_width

    global contents
    contents += "<h2>Event date: " + event_date + "</h2>"
    contents += "<table width = " + str(table_width) + "%><th><tr style=height: 1px;>"
    for _ in range(max_crew_size + 1):
        contents += "<td width = " + str(column_width) + "%></td>"
    contents += "</tr></th>"
    for crew in crews:
        contents += "<tr><td>" + crew["boat"]["display name"] + "</td>"
        for sailor in crew["sailors"]:
            contents += "<td>" + sailor["display name"] + "</td>"
        empty_cells = max_crew_size - len(crew["sailors"])
        for _ in range( empty_cells ):
            contents += "<td>" + "" + "</td>"
        contents += "</tr>"
    contents += "<tr><td>" + "Wait list" + "</td>"
    for sailor in wait_list:
        contents += "<td>" + sailor["display name"] + "</td>"
    empty_cells = max_crew_size - len(wait_list)
    for _ in range( empty_cells ):
        contents += "<td>" + "" + "</td>"
    contents += "</tr></table>"
    contents += "<h3>Non-compliance: " + crews_score + "</h3>"
    contents += "<hr>"

    html = top + contents + tail

    return html
