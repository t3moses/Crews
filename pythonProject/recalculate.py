
#!.venv/bin/python3.12

import database
import assignment
import crew_html

database.begin()
crew_html.begin()

assignment.assignment()

database.end()
