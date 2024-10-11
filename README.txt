assign.py assigns available sailors to available boats.

There are two classes of assignment rule: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particuar day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally.

Discretionary rules calculate a non-compliance score, which can be used to select a satisfactory assignment.

Mandatory requirements:

- members shall take priority over non-members;
- sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times;
- boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.

Discretionary requirements:

- partners should not be assigned to the same boat;
- sailors should be assigned to the same boat as few times as possible throughout the season;
- sailors should only be assigned to boats on their white-list.
- the skill-spread on a boat should be as small as possible;
- skippers requiring assistance should be assigned at least one sailor from the highest skill band.


