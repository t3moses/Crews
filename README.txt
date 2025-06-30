Crew assignment

assignment.py assigns available sailors to available boats for future event dates.

Assignment is governed by two classes of assignment rules: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally, and so they are fully enforced.

Discretionary rules calculate a "non-compliance" score.  The score is used to select a suitably compliant assignment.  Discretionary rules are applied with best effort.  
A gradient-descent algorithm finds a local minimum.  But a solution with lower score may exist globally.

Mandatory rules:

- Members shall take priority over non-members;
- All boats shall reach (at least) their minimum occupancy.
- No boat shall exceed its maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking into account their maximum capacities.
- Sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times.
- Boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.
- Sailors (members or non-members) who have been assigned a space seven days ahead of an event will not lose their space,
  even if higher-priority sailors enrol in the interim.  This rule does not apply in case a boat withdraws.

Discretionary rules (in priority order):

- Skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- Sailors should only be assigned to boats on their white-list.
- The skill-spread on a boat should not exceed two bands;
- Members of a partnership should not be assigned to the same boat.
- Sailors should be assigned to the same boat as few times as possible throughout the season.

Neural network

Once the mandatory rules have been applied, crews are ordered by their non-compliance score.

The crew with the highest score is selected, every possible swap of sailors between this crew
and the remaining crews is made and the loss recalculated for each swap.  The swap with the lowest loss is retained.
Then the process is repeated a set number of times.

This may only find a local minimum.  By randomizing the initial conditions and repeating, a more compliant solution may be found.

Input files

Inputs are taken from the following files.

boats data.csv
sailors data.csv
boats available.csv
sailors available.csv
sailor histories.csv
user input.txt

With the exception of the user input file, these files are formatted as CSV.  In this way, they may be edited in a text editor or a spreasheet program.

In the event these files don't exist in the expected location, when the process.py script runs, it creates them.  The expected location is a hard-wired constant.

The list of event dates is a constant in the constants.py file.

The boats ... files contain a row for each boat.
The sailors ... files contain a row for each sailor.
The ... available files contain the dates on which the subject (boat or sailor) is available.

The boat assistance field contains True or False according to whether the skipper requires assistance on board.
The sailor member field contains True or False according to whether the sailor is an NSC member.
The skill field contains integer values 0 .. 2.  0 for novice, 1 for basic qualified, 2 for experienced.
The whitelist field contains a list of boats in the subject's whitelist.  Boats in the list must be separated by ;.

In the sailor resume field, commas and newlines are escaped.

Outputs

The final crew is saved as an HTML table.  The HTML table should be pasted to the web-site event calendar iFrame.
In case the number of sailors is greater than the available spaces, then the wait list is included in the output table.

User interactions

The program description web page includes links for registration as a:

Boat owner
crew member

And a link to the event calendar.

Registration involves opening an account and setting initial availability for program events.

If the registrant's availability changes, it can be updated without reopening the account.

Clicking the update button causes an email to be sent to the admin.

Set-up

Some or all of the files may be created using a text editor or spreadsheet program.  In case they don't exist, they will be created when the script runs.

The program checks the consistency of the boat names, sailor names and event dates amongst the files.  It raises an exception if an inconsistency is encountered.

In-season changes

In case boats or sailors drop out during the season, no action is required; their entries can remain in the database without causing harm.

Boats and sailors added during the season will replace any with the identical boat name or sailor name, respectively.

Operating environment

Install Python Launcher.

Set the default application for all files with the .py extension to Python Launcher.

Configure Python Launcher to 

	✓  Allow override with #! in script
	✓  Run in a terminal window

Copy the Python and config files to a folder.

Double-click the process.py file.

Double-clicking recalculate.py refreshes the assignments.html file without importing new boat or sailor data.
This is useful if any of the .csv files have been edited directly.

Self-service web-site

The application works in conjunction with a Wixstudio web-site.  Boat owners and sailors provide information for the application using web forms.

When the admin receives an email, they must save it in plain-text to a folder called User input.  Old files are replaced when a new one is saved.

It appears that registration forms submitted while the admin is logged-on may NOT produce email notifications.  Therefore, processing registrations should be performed quickly, seldom and outside peak times.

Process

The calendar is updated in one of two ways.

process.py processes the contents of the email sent to the admin when a boat-owner or sailor submits a form.  It updates the database files described above.

recalculate.py updates the calendar without processing an email.

Boat owners and sailors should open an account.  This allows them to enter information about themselves and their boat.

In the event they don't open an account, they may continue as a guest, with default values.

They must also enter information about their availability.

An individual may enrol as both a boat owner and a sailor.  In the event of an availability clash, their boat owner role takes precedence.

When a boat-owner enrols, the admin is asked if the owner is female.  This information is used in support of the policy that places women who request it be assigned to boats skippered by a woman.

When a sailor enrols, the admin is asked for the display name of the sailor's partner.  This information is used in support of the policy that places partners on different boats.

A sailor display name comprises their first name, capitalized, concatenated with the fewest number of character from their last name, again capitalized, to make the display name unique.

There is no live connection between front and back end.  So user input is required to correlate account and availability information.  Correlation is based on a key.

The key comprises the first and last names, concatenated and all lowercase.  Therefore, the spelling must be identical in each interaction.

Event calendar

The event calendar contains the assignments for the season, based on the current registered boats and sailors.

process.py creates a file called assignments.html in the html folder.  This must be opened in a text editor, copied and pasted into the iframe of the calendar page.

Over-capacity

In the event that there are insufficient crew to meet the minimum required for the flotilla, boats are removed from the flotilla repeatedly until the minimum is equal to or less than the number of crew.
First of all, boats whose skippers have also enrolled as sailors are removed.  Then boats that have sailed fewest times in the season are removed.

No-shows

Sailors who fail to show-up or cancel later than 10:00 am on the day of the event may be deprioritized for future events.

This is effected by changing 'A' in their availability record to 'N'.

Data structures

An important data structure is the event:

event {
 date
 flotilla [
   { boat
     sailors [
      (sailor)
     ]
   }
 ]
 wait list [
  (sailor)
 ]
}

Version control

The Git repository is here:

https://github.com/t3moses/Crews

Reports

process.py and recalculate.py create reports:

1. address.txt contains the email addresses of participants in all future events, separating boat owners from sailors.

2. crew_info.txt contains the resumes of sailors in the next event organized by boat.

The latter is intended to be provided to the boat owners taking part in the upcoming event.

3. debug.txt lists the non-compliance scores for each iteration and each event date.  It also lists the causes of non-compliance in the final assignment.

