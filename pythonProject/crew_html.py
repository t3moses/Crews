import constants

top = ""
tail = ""
contents = ""

def begin():

    global top
    top += "<!DOCTYPE html><html><head><style>"
    top += "table {font-family: arial, sans-serif;border-collapse: collapse;}"
    top += "td {border: 1px solid #dddddd;text-align: left;padding: 8px;}"
    top += "tr:nth-child(even) {background-color: #dddddd;}"
    top += "</style></head><body>"

    global tail
    tail += "</body></html>"

    return

def html(scored_crews, wait_list, event_date):

    crews = scored_crews["crews"]
    loss = scored_crews["crews score"]

    max_crew_size = 0
    for crew in crews:
        crew_size = len(crew["sailors"])
        if crew_size > max_crew_size:
            max_crew_size = crew_size
    crew_size = len(wait_list)
    if crew_size > max_crew_size:
        max_crew_size = crew_size

    number_of_columns = max_crew_size + 1
    max_number_of_columns = constants.max_number_of_crew + 1
    table_width = str(int(100 * number_of_columns / max_number_of_columns))
    column_width = str(int(100 / number_of_columns))
    """
    top = ""
    top += "<!DOCTYPE html><html><head><style>"
    top += "table {font-family: arial, sans-serif;border-collapse: collapse;width: " + table_width + "%;}"
    top += "td {""width: " + column_width + "%;border: 1px solid #dddddd;text-align: left;padding: 8px;}"
    top += "tr:nth-child(even) {background-color: #dddddd;}"
    top += "</style></head><body>"

    tail = ""
    tail += "</body></html>"
    """
    global contents
    contents += "<h2>Event date: " + event_date + "</h2>"
    contents += "<table width = table_width><th><tr style=""height: 1px;"">"
    for _ in range(number_of_columns):
        contents += "<td width = column_width></td>"
    contents += "</tr></th>"
    for crew in crews:
        contents += "<tr><td>" + crew["boat"]["boat name"] + "</td>"
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
    contents += "<h3>Non-compliance: " + loss + "</h3>"
    contents += "<hr>"

    html = top + contents + tail

    return html
