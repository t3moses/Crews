Crew assignment

assignment.py assigns available sailors to available boats for a specific event date.

Assignment is governed by two classes of assignment rules: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally, and so they are fully enforced.

Discretionary rules produce a "non-compliance" score.  The score is used to select a suitably compliant assignment.  Discretionary rules are applied with best effort.  
A gradient-descent algorithm finds a local loss minimum.  But a solution with lower score may exist globally.

Mandatory rules:

- Members shall take priority over non-members;
- All boats shall reach (at least) their minimum occupancy.
- No boat shall exceed its maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking into account their maximum capacities.
- Sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times.
- Boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.

Discretionary rules:

- Sailors should only be assigned to boats on their white-list.
- Skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- The skill-spread on a boat should not exceed two bands;
- Sailors should be assigned to the same boat as few times as possible throughout the season.
- Members of a partnership should not be assigned to the same boat.

Machine-learning

Once the mandatory rules have been applied, crews are ordered by their non-compliance score.

The two crews with the highest score are selected, every possible swap of sailors between those two crews
is made and the loss recalculated for each swap.  The swap with the lowest loss is retained.
Then the process is repeated a set number of times.

Input files

Inputs are taken from the following files.

boats data.txt
sailors data.txt
boats available.txt
sailors available.txt
sailor histories.txt
user input.txt

With the exception of the user input file, these files are formatted as CSV.  In this way, they may be edited in a text editor or a spreasheet program.

In the event these files don't exist in the expected location, when the process.py script runs, it creates them.  The expected location is a hard-wired constant.

The list of event dates is a constant in the constants.py file.

The boats ... files contain a row for each boat.
The sailors ... files contain a row for each sailor.
The ... available files contain the dates on which the subject (boat or sailor) is available.

The sailor assistance field contains True or False according to whether the skipper requires assistance on board.
The member field contains True or False according to whether the sailor is an NSC member.
The skill field contains integer values 0 .. 2.  0 for novice, 1 for basic qualified, 2 for experienced.
The whitelist field contains a list of boats in the subject's whitelist.  Boats in the list must be separated by ;.

In the sailor resume field, commas and newlines are escaped.

Outputs

The final crew is saved as an HTML table.  The HTML table should be pasted to the web-site event calendar iFrame.
In case the number of sailors is greater than the available spaces, then the wait list is included in the output table.

User interactions

The program description web page provides links to web forms for submitting:

Boat information
Sailor information
Boat availability
Sailor availability
Event calendar

The first four of these contain a "Submit" button.  Clicking this causes an email to be sent to the admin.

Set-up

Some or all of the files may be created using a text editor or spreadsheet.  In case they don't exist, they will be created when the script runs.

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

Self-service web-site

The application works in conjunction with a Wix web-site.  Boat owners and sailors provide information for the application using web forms.

The email must be saved in plain text to a specific folder.  Old files are deleted when a new one is processed.

Process

process.py processes the contents of the email sent to the admin when a boat-owner or sailor submits a form.  It updates the database files described above.

Four types of form are processed.

Boat owners and sailors should open an account.  This allows them to enter information about themselves and their boat.

In the event they don't open an account, they may continue as a guest, with default values.

In a seprate step, they must enter information about their availability.

An individual may enrol as both a boat owner and a sailor.  In the event of an availability clash, their boat owner role takes precedence.

When a boat-owner enrols, the admin is asked if the owner is female.  This information is used in support of the policy that places women who request it be assigned to boats skippered by a woman.

When a sailor enrols, the admin is asked for the display name of the sailor's partner.  This information is used in support of the policy that places partners on different boats.

There is no connection between front and back end.  So user input is required to correlate account and availability information.  Correlation is based on first and last name.  Therefore, the spelling must be identical in each interaction.

Event calendar

The event calendar contains the assignments for the season, based on the current registered boats and sailors.

The calendar also shows the non-conformance score for each event.  Single-digit scores are generally acceptable.  But, double-digit scores are likely to be encountered, particularly towards the end of the season.

Data structures

An important data structure is the flotilla:

flotilla {
  crews [
    (crew) {
      boat
      sailors [
        (sailor) {}
      ]
      score
    }
  ]
  wait list [
    (sailor) {}
  ]
  score
}

To dos

- Randomize the list of boats and sailors between passes in the outler loop after it has been determined which boats and sailors will sail in a particular event.
- Create reports, including:
	owner email addresses for an event
	sailor email addresses for an event
	sailor resumes by boat for an event
- Specify the Working directory in the constants.py file.
	

