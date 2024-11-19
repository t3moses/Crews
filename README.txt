Assignment

assignment.py assigns available sailors to available boats for a specific event date.

Assignment is governed by two classes of assignment rules: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally, and so they are fully enforced.

Discretionary rules cause a "loss" calculation.  The loss can be used to select the most compliant assignment.  As such, discretionary rules are applied with best effort.  
A gradient-descent algorithm finds a local loss minimum.  But a solution with lower loss may exist globally.

Mandatory requirements:

- Members shall take priority over non-members;
- All boats shall meet (at least) their minimum occupancy.
- All boats shall meet (at most) their maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking into account their maximum occupancies.
- Sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times.
- Boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.

Discretionary requirements:

- Sailors should only be assigned to boats on their white-list.
- Skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- The skill-spread on a boat should be as small as possible;
- Sailors should be assigned to the same boat as few times as possible throughout the season.
- Members of a partnership should not be assigned to the same boat.

Machine-learning

Once the mandatory rules have been applied, crews are ordered by their loss value.

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

Each of these files is formatted as CSV.  In this way, they may be edited in a text editor or a spreasheet program.  The first row contains the field names, as follows:

boats data.txt: boat name,owner display name,owner email address,mobile,female,min_occupancy,max_occupancy,request assist
sailors data.txt: display name,partner,email address,member,skill,experience,request female,whitelist
boats available.txt: boat name,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26
sailors available.txt: display name,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26
sailor histories.txt: display name,Fri Jun 6,Fri Jun 13,Fri Jun 20,Sat Jun 28,Fri Jul 4,Fri Jul 11,Sat Jul 19,Fri Jul 25,Fri Aug 1,Sat Aug 9,Fri Aug 15,Fri Aug 22,Sat Aug 30,Fri Sep 5,Fri Sep 12,Fri Sep 19,Fri Sep 26

The list of event dates is a constant in the constants.py file.

The boats ... files contain a row for each boat.
The sailors ... files contain a row for each sailor.
In the ... available files contain the dates on which the subject (boat or sailor) is available.

The request assist field contains True or False according to whether the skipper requires assistance on board.
The member field contains True or False according to whether the sailor is an NSC member.
The skill field contains integer values 0 .. 2.  0 for novice, 1 for basic qualified, 2 for experienced.
The whitelist field contains a list of boats in the subject's whitelist.  Boats in the list must be separated by ;.

The sailor display name should be unique.  It is formed from the first name and the initial letter of the last name.  
The first letter of the first name and the initial of the last name are uppercase.  All other letters are lower case.  
In case of a clash, an exception is raised.

Outputs

A graph of loss against epoch is displayed.

The final crew is saved as an HTML table.  (This can be cut-and-pasted into a Web page iFrame.)
In case the number of sailors is greater than the available spaces, then the wait list is included in the output table.

The HTML table should be pasted to the appropriate event calendar iFrame.

User interactions

The Wix program description web page contains links to the following functions:

Enrol a boat
Enrol a sailor
Register a boat
Register a sailor
Event calendar

The first four of these contain a "Submit" button.  Clicking this causes an eamil to be sent to the admin.

Set-up

Use a text editor or spreadsheet program to create the following files:

boats data.txt // This is the authoritative source of boat data, including names.
sailors data.txt // This is the authoritative source of sailor data, including names.

The following files may be created using a text editor or spreadsheet.  In case they don't exist, they will be created when the program runs.
However, files created in this way will contain no availability data.

boats available.txt
sailors available.txt

The program checks the consistency of the boat names, sailor names and event dates amongst these files.  It raises an exception if an inconsistency is encountered.

Boats' availability and sailors' availability may be entered manually into boats available.txt and sailors available.txt.  Alternatively, see Process, below.

The program will write assignments into the sailor histories.txt file.  If this file does not exist, it will be created.

In-season changes

In case boats or sailors drop out during the season, no action is required; their entries can remain in the database without harm.

Boats and sailors added during the season will replace any with the identical boat name or display name, respectively.

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

The user is asked to input an event id.  This should be in the format date + "v" + version.  The date is checked against the set of event dates.
In case it is not a member of the set, an exception will be raised.  The event id seeds the random number generator.  In this way,
re-using an event id generates the same output.  But, different outputs result for the same date if the version is changed.

Process

process.py processes the contents of the email sent to the admin when a boat-owner or sailor submits a form.  It updates the database files described above.

Four types of form are processed:

Enrol a boat
Enrol a sailor
Register a boat
Register a sailor

Boat-owners and sailors enrol in the PROGRAM for the season.  Then they REGISTER for specific event dates.

An individual may enrols as both a boat owner and a sailor.  In the event of an availability clash, their boat owner role takes precedence.

When a boat-owner enrols, the admin is asked if the owner is female.  This information is used in support of the policy that places women who request it be assigned to boats skippered by a woman.

When a sailor enrols, the admin is asked for the display name of the sailor's partner.  This information is used in support of the policy that places partners on different boats.

There is no connection between front and back end.  So user input is required to correlate enrolment and registration events.  Correlation is based on first and last name.  Therefore, the spelling must be identical in each interaction.

Event calendar

The event calendar contains the assignments for the season, based on the current registered boats and sailors.

The calendar also shows the non-conformance score (or loss).  Single-digit scores are generally acceptable.  But, double-digit scores should prompt a rerun with a different event_id.




