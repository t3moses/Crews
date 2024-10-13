assign.py assigns available sailors to available boats.

There are two classes of assignment rule: mandatory rules and discretionary rules.

Mandatory rules determine which boats and sailors will sail on a particular day.

Discretionary rules determine which boat a particular sailor will be assigned to.

Mandatory rules are executed procedurally.

Discretionary rules calculate a non-compliance score, which can be used to select a satisfactory assignment.

Mandatory requirements:

- members shall take priority over non-members;
- sailors who have sailed fewer times in the current season of the program shall take priority over those who have sailed more times;
- boats that have sailed fewer times in the current season of the program shall take priority over those that have sailed more times.
- All boats shall have at least their minimum occupancy.
- All boats shall have no more than their maximum occupancy.
- Sailors shall be distributed evenly across all boats, taking accont of their maximum occupancies.

Discretionary requirements:

- sailors should only be assigned to boats on their white-list.
- partners should not be assigned to the same boat;
- skippers requiring assistance should be assigned at least one sailor from the highest skill band;
- the skill-spread on a boat should be as small as possible;
- sailors should be assigned to the same boat as few times as possible throughout the season.

Machine-learning

Once the mandatory rules have been appied, crews are ordered by score.

The two crews with the highest non-compliance scores are selected, every possible swap of crew
is made and a crew score recalculated for each swap.  The swap with the lowest non-compliance
score is retained.  Then the process is repeated a set number of time.