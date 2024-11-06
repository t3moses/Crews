
def html(crews, wait_list, event_date):
    
    max_crew_size = 0
    for crew in crews:
        crew_size = len(crew["sailors"])
        if crew_size > max_crew_size:
            max_crew_size = crew_size
    crew_size = len(wait_list)
    if crew_size > max_crew_size:
        max_crew_size = crew_size

    top = "<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 50%;}td {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"
    top += "<h2>Event date: " + event_date + "</h2><table>"
    tail = "</table></body></html>"
    contents = ""
    for crew in crews:
        contents += "<tr><td>" + crew["boat"]["name"] + "</td>"
        for sailor in crew["sailors"]:
            contents += "<td>" + sailor["name"] + "</td>"
        empty_cells = max_crew_size - len(crew["sailors"])
        for _ in range( empty_cells ):
            contents += "<td>" + "" + "</td>"
        contents += "</tr>"
    contents += "<tr><td>" + "Wait list" + "</td>"
    for sailor in wait_list:
        contents += "<td>" + sailor["name"] + "</td>"
    empty_cells = max_crew_size - len(wait_list)
    for _ in range( empty_cells ):
        contents += "<td>" + "" + "</td>"
    contents += "</tr>"
    html = top + contents + tail
    return html
