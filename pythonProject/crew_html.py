
def html(crews, event_date):

    top = "<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 50%;}td {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body>"
    top += "<h2>Event date: " + event_date + "</h2><table>"
    tail = "</table></body></html>"
    contents = ""
    for crew in crews:
        contents += "<tr><td>" + crew["boat"]["name"] + "</td>"
        for sailor in crew["sailors"]:
            contents += "<td>" + sailor["name"] + "</td>"
        contents += "</tr>"
    html = top + contents + tail
    return html
