assign.py assigns available sailors to available boats.

There are two classes of assignment rules: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally and they are fully enforced.

Discretionary rules calculate a non-compliance score, which can be used to select a satisfactory assignment.
So, they are applied with best effort.

Mandatory requirements:

- Members shall take priority over non-members;
- All boats shall have at least their minimum occupancy.
- All boats shall have no more than their maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking accont of their maximum occupancies.
- Sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times;
- Boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.

Discretionary requirements:

- Sailors should only be assigned to boats on their white-list.
- Partners should not be assigned to the same boat;
- Skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- The skill-spread on a boat should be as small as possible;
- Sailors should be assigned to the same boat as few times as possible throughout the season.

Machine-learning

Once the mandatory rules have been applied, crews are ordered by non-compliance score.

The two crews with the highest non-compliance scores are selected, every possible swap of crew
is made and a crew score recalculated for each swap.  The swap with the lowest non-compliance
score is retained.  Then the process is repeated a set number of times.

Input files

Inputs are taken from the following files.

boats data.txt
sailors data.txt
boats availability.txt
sailors availability.txt
sailor histories.txt

Each of these files is formatted as CSV.  The first row contains the field names, as follows:

boats data.txt: name,owner,slip,min_occupancy,max_occupancy,assist
sailors data.txt: name,partner,member,skill,whitelist
boats availability.txt: name,06-06,06-13,06-20,06-28,07-04,07-11,07-19,07-25,08-01,08-09,08-15,08-22,08-30,09-05
sailors availability.txt: name,06-06,06-13,06-20,06-28,07-04,07-11,07-19,07-25,08-01,08-09,08-15,08-22,08-30,09-05
sailor histories.txt: name,06-06,06-13,06-20,06-28,07-04,07-11,07-19,07-25,08-01,08-09,08-15,08-22,08-30,09-05

The authoritative list of event dates is taken from the boats availability.txt file.

The boats ... files contain a row for each boat.
The sailors ... files contain a row for each sailor.
In the ... availability files, a non-empty field indicates the dates on which the subject is available.

The assist field contains True or False according to whether the skipper requires assistance or not.
The member field contains True or False according to whether the sailor is a member or not.
The skill field contains integer values 0 .. 2.  0 for novice, 1 for basic qualified, 2 for experienced.
The whitelist field contains a list of boats in the subject's whitelist.  Boats in the list must be separated by ;.

Set-up

Use a text editor or spreadsheet program to create the following files:

boats data.txt // This is the authoritative source of boat data.
sailors data.txt // This is the authoritative source of sailor data.
boats availability.txt // This is the authoritative source of event dates.
sailors availability.txt
sailor histories.txt

The program checks the consistency of the boat data, sailor data and event dates amongst these files.  It raises an exception if an inconsistency is encountered.

Boats availability and sailors availability must be entered manually into boats availability.txt and sailors availability.txt.

The program will write assignments into the sailor histories.txt file.

Output

for crew in crews:
	for sailor in crew:
		sailor_histories["name" : sailor["name"]][event_date] = crew["boat"]["name"]


with open(Working_directory+"config.txt", "r") as f_config:
    ...
    s_line_5 = f_config.readline() # sailors history

sailor_histories_filename = Working_directory+s_line_5.split(': ')[1].split(' //')[0]

update sailor_history in sailor_histories

sailor_histories_file = open(sailor_histories_filename, 'w', newline='')

csv_writer = csv.DictWriter(sailor_histories_file, fieldnames=event_dates)
make header row from "name" and event dates
writer.writeheader()
for sailor_history in sailor_histories:
    make sailor row from history and crew
    csv_writer.writerow( dict ) # sailor row
sailor_histories_file.close()



