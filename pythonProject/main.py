#!.venv/bin/python3.12

import csv

week = input("Enter week number :")

Working_directory = "/Users/timmoses/Documents/Tech/Projects/Version_controlled/Assignment/Config/"

with open(Working_directory+"config.txt", "r") as f_config:
    s_line_1 = f_config.readline() # boats data
    s_line_2 = f_config.readline() # sailors data
    s_line_3 = f_config.readline() # boats availability
    s_line_4 = f_config.readline() # sailors availability

boats_data_filename = Working_directory+s_line_1.split(': ')[1].split(' //')[0]
sailors_data_filename = Working_directory+s_line_2.split(': ')[1].split(' //')[0]
boats_available_filename = Working_directory+s_line_3.split(': ')[1].split(' //')[0]
sailors_available_filename = Working_directory+s_line_4.split(': ')[1].split(' //')[0]

boat_data_dicts = []
with open(boats_data_filename) as boats_data_file:
    boats_data = csv.DictReader(boats_data_file)
    for boat in boats_data:
        boat_data_dicts.append(boat)

for i in range(len(boat_data_dicts)):
    print(boat_data_dicts[i])

boat_available_dicts = []
with open(boats_available_filename) as boats_available_file:
    boats_available = csv.DictReader(boats_available_file)
    for boat in boats_available:
        boat_available_dicts.append(boat)

for i in range(len(boat_available_dicts)):
    print(boat_available_dicts[i])

sailor_data_dicts = []
with open(sailors_data_filename) as sailors_data_file:
    sailors_data = csv.DictReader(sailors_data_file)
    for sailor in sailors_data:
        sailor_data_dicts.append(sailor)

for i in range(len(sailor_data_dicts)):
    print(sailor_data_dicts[i])

sailor_available_dicts = []
with open(sailors_available_filename) as sailors_available_file:
    sailors_available = csv.DictReader(sailors_available_file)
    for sailor in sailors_available:
        sailor_available_dicts.append(sailor)

for i in range(len(sailor_available_dicts)):
        print(sailor_available_dicts[i])

'''
with open(Working_directory+'history.csv', 'w', newline='') as history_file:
    fieldnames = ['name', '1', '2']
    writer = csv.DictWriter(history_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(len(sailor_data_dicts)):
        writer.writerow({'name': sailor_data_dicts[i]['name']})
'''
