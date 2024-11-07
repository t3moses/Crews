assignment.py assigns available sailors to available boats.

There are two classes of assignment rules: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally and they are fully enforced.

Discretionary rules calculate a loss, which can be used to select a satisfactory assignment.  So, they are applied with best effort.  
The gradient-descent algorithm finds a local loss minimum.  A solution with lower loss may exist globally.

Mandatory requirements:

- Members shall take priority over non-members;
- All boats shall have at least their minimum occupancy.
- All boats shall have no more than their maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking accont of their maximum occupancies.
- Sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times.
- Boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.

Discretionary requirements:

- Sailors should only be assigned to boats on their white-list.
- Skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- The skill-spread on a boat should be as small as possible;
- Sailors should be assigned to the same boat as few times as possible throughout the season.

Members of a partnership are treated as independent, so that they MAY be assigned to the same boat,
but this is no more or less likely than their being assigned to the same boat as a sailor who is not
their partner.

Machine-learning

Once the mandatory rules have been applied, crews are ordered by their loss.

The two crews with the highest loss are selected, every possible swap of sailors
is made and the loss recalculated for each swap.  The swap with the lowest loss is retained.
Then the process is repeated over a set number of epochs.

Input files

Inputs are taken from the following files.

boats data.txt
sailors data.txt
boats available.txt
sailors available.txt
sailor histories.txt

Each of these files is formatted as CSV.  The first row contains the field names, as follows:

boats data.txt: boat name,owner email address,min_occupancy,max_occupancy,assistance request
sailors data.txt: first name,last name,email address,uid,display name,member,skill,whitelist
boats available.txt: boat name,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26
sailors available.txt: uid,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26
sailor histories.txt: uid,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26

The list of event dates is a constant.

The boats ... files contain a row for each boat.
The sailors ... files contain a row for each sailor.
In the ... available files, a non-empty field indicates the dates on which the subject is available.

The assist field contains True or False according to whether the skipper requires assistance or not.
The member field contains True or False according to whether the sailor is an NSC member or not.
The skill field contains integer values 0 .. 2.  0 for novice, 1 for basic qualified, 2 for experienced.
The whitelist field contains a list of boats in the subject's whitelist.  Boats in the list must be separated by ;.

The sailor display name is unique.  It is formed from the first name and the initial letter of the last name.  The first letter of the first name and the initial of the last name are uppercase
All other letters are lower case.  In case of a clash, an exception is raised.

The sailor uid is unique.  It is formed from the initial letter of the first name and the first three letters of the last name.
All letters are lower case.  And any non-alphabet character is deleted.

Outputs

A graph of loss against iteration is displayed.

The final crew is saved as an HTML table.  (This can be cut-and-pasted into a Web page iFrame.)
In case the number of sailors is greater than the available spaces, then the wait list is included in the output table.

Set-up

Use a text editor or spreadsheet program to create the following files:

boats data.txt // This is the authoritative source of boat data, including names.
sailors data.txt // This is the authoritative source of sailor data, including names.

The following files may be created using a text editor or spreadsheet.  In case they don't exist, they will be created when the program runs.
However, files created in this way will contain no availability data.

boats available.txt
sailors available.txt

The program checks the consistency of the boat names, sailor names and event dates amongst these files.  It raises an exception if an inconsistency is encountered.

Boats' availability and sailors' availability must be entered manually into boats available.txt and sailors available.txt.

The program will write assignments into the sailor histories.txt file.  If this file does not exist, it will be created.

In-season changes

In case boats or sailors drop out during the season, no action is required.

In case boats join during the season, their details must be added manually to boats data.txt and boats available.txt.

In case sailors join during the season, their details must be added manually to sailors data.txt, sailors available.txt and sailor histories.txt.

The program will detect inconsistencies and raise an exception if any are discovered.

Operating environment

Install Python Launcher.

Set the default application for all files with the .py extension to Python Launcher.

Configure Python Launcher to 

	✓  Allow override with #! in script
	✓  Run in a terminal window

Copy the Python and config files to a folder.

Double-click assignment.py.

Run

The user is asked to input an event id.  This should be in the format date.version.  The date is checked against the set of event dates.
In case it is not a member of the set, an exception will be raised.  The event id seeds the random number generator.  In this way,
re-using an event id generates the same output.  But, different outputs result for the same date if the version is changed.

