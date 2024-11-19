import constants
def html(scored_crews, wait_list, event_date):

    crews = scored_crews["crews"]
    loss = scored_crews["loss"]

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

    event_version = "0"

    top = ""
    top += "<!DOCTYPE html><html><head><style>"
    top += "table {font-family: arial, sans-serif;border-collapse: collapse;width: " + table_width + "%;}"
    top += "td {""width: " + column_width + "%;border: 1px solid #dddddd;text-align: left;padding: 8px;}"
    top += "tr:nth-child(even) {background-color: #dddddd;}"
    top += "</style></head><body>"
    top += "<h2>Event date: " + event_date + "</h2>"
    top += "<table><th><tr style=""height: 1px;"">"
    for _ in range(number_of_columns):
        top += "<td></td>"
    top += "</tr></th>"

    tail = "</table>"
    tail += "<h2>Version: " + event_version + "</h2>"
    tail += "<h2>Non-compliance: " + loss + "</h2>"
    tail += "</body></html>"

    contents = ""
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
    contents += "</tr>"
    html = top + contents + tail

    return html
