# Assignment script

import csv

Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/Config/"

with open(Working_directory+"config.txt", "r") as f_config:
    s_line_1 = f_config.readline()
    s_line_2 = f_config.readline()

boats_filename = Working_directory+s_line_1.split(': ')[1].split(' //')[0]
sailors_filename = Working_directory+s_line_2.split(': ')[1].split(' //')[0]

boat_dicts = []
with open(boats_filename) as boats_file:
    boats = csv.DictReader(boats_file)
    for boat in boats:
        boat_dicts.append(boat)
print(boat_dicts[0]['name'])
