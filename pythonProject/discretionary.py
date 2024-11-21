
import random
import copy
import constants

def discretionary(crews, sailor_histories, event_date):

    # Add the crew non-compliance score for each crew to its dictionary.
    # Calculate the overall non-compliance score for the flotilla.
    # Order the crews by increasing non-compliance score and call swap.
    # Repeat multiple times and calculate the resulting overall score.

    for crew in crews:
        crew["crew score"] = crew_score(crew, sailor_histories, event_date)

    crews = order_crews_by_score(crews)

    best_crews = []

    for _ in range(constants.inner_epochs):
        crews_score = 0
        for crew in crews:
            crews_score += int(crew["crew score"])

        best_crews = swap(crews, sailor_histories, event_date)

    scored_crews = {}
    scored_crews["crews"] = best_crews
    scored_crews["crews score"] = str(crews_score)

    return scored_crews

def crew_score(crew, sailor_histories, event_date):

    # Calculate the non-compliance score for one crew.

    whitelist_score = constants.whitelist_weight * whitelist(crew)
    partner_score = constants.partner_weight * partner(crew)
    assist_score = constants.assist_weight * assist(crew)
    skill_score = constants.skill_weight * skill(crew)
    repeat_score = constants.repeat_weight * repeat(crew, sailor_histories, event_date)

    crew_score = whitelist_score + partner_score + assist_score + skill_score + repeat_score

    return crew_score

def whitelist(crew):

    # Count the number of times the boat is not on a sailor's whitelist.

    crew_score = 0

    boat_name = crew["boat"]["boat name"]
    for sailor in crew["sailors"]:
        whitelist = sailor["whitelist"]
        if whitelist.count(boat_name) == 0:
            crew_score += 1

    return crew_score

def partner(crew):

    # Count the number of times a sailor is sailing with their partner.

    crew_score = 0

    for sailor_1 in crew["sailors"]:
        for sailor_2 in crew["sailors"]:
            if sailor_1["partner"] == sailor_2["display name"]:
                crew_score += 1

    return crew_score

def assist(crew):

    # Identify if a boat requiring assistance does not have a sailor with skill level 2.

    if crew["boat"]["request assist"] == "True":
        crew_score = 1

        for sailor in crew["sailors"]:
            if int(sailor["skill"]) == 2:
                crew_score = 0
    else:
        crew_score = 0

    return crew_score

def skill(crew):

    # Identify if the spread of skill levels on the boat is greater than 1.

    max_skill = 0
    min_skill = 2

    for sailor in crew["sailors"]:
        max_skill = max( int(sailor["skill"]), max_skill)
        min_skill = min( int(sailor["skill"]), min_skill)
    spread = max_skill - min_skill
    if spread > 1:
        crew_score = 1
    else:
        crew_score = 0

    return crew_score

def repeat(crew, sailor_histories, event_date):

    # Calculate a score based on  how recently each sailor has sailed on the current boat.

    crew_score = 0
    for sailor in crew["sailors"]:
        for sailor_history in sailor_histories:
            if sailor_history["display name"] == sailor["display name"]:
                for date in constants.event_dates:
                    if date == event_date:
                        break
                    else:
                        if sailor_history[date] == crew["boat"]["boat name"]:
                            contribution = pow(constants.event_dates.index(event_date) - constants.event_dates.index(date), constants.repeat_exponent)
                            crew_score += contribution
    return int(crew_score)


def order_crews_by_score(crews):

    # Create a list that orders crews by their non-compliance score.
    # The order of crews in the same score band is randomized.

    ordered_crews = []
    banded_crews = []

    i = len(crews)
    crew_score = 0
    while i > 0:
        equal_crews = [] # list of boats in the same score band.
        for crew in crews:
            if int(crew["crew score"]) == crew_score:
                equal_crews.append(crew)
                i -= 1
        crew_score += 1
        banded_crews.append(equal_crews)

    while len(banded_crews) > 0:
        while len(banded_crews[0]) > 0: # There are one or more sailors in the crew.
            if len(banded_crews[0]) > 1:
                boat_number = random.randint(0, len(banded_crews[0]) - 1)
            else:
                boat_number = 0
            ordered_crews.append(banded_crews[0][boat_number])
            banded_crews[0].pop(boat_number)
        banded_crews.pop(0)

    return ordered_crews

def swaps(crews, sailor_histories, event_date):

    for _ in range(5):

        crews = swap(crews, sailor_histories, event_date)

    return crews

def swap(crews, sailor_histories, event_date):

    # The received crews list contains a list of crews in increasing non-compliance order.
    # Hence, the last two entries have the highest non-compliance scores.
    # Calculate the initial non-compliance score for the flotilla.
    # From crews, select the two crews with the highest non-compliance scores.
    # Swap a pair of sailors between these two crews.
    # Calculate the new non-compliance score.
    # Repeat for each pair of sailors, recording the resulting non-compliance scores.
    # If the best swap is not worse than the original, update crews.

    global best_i, best_j
    initial_score = 0
    for crew in crews:
        initial_score += crew["crew score"]
    best_score = initial_score

    for i in range (len(crews[-2]["sailors"])):
        for j in range (len(crews[-1]["sailors"])):
            candidates = copy.deepcopy(crews)
            parked_sailor = candidates[-2]["sailors"][i].copy()

            candidates[-2]["sailors"].pop(i)
            candidates[-2]["sailors"].insert(i, candidates[-1]["sailors"][j])
            candidates[-1]["sailors"].pop(j)
            candidates[-1]["sailors"].insert(j, parked_sailor)
            candidates_score = 0
            for candidate in candidates:
                candidates_score += crew_score(candidate, sailor_histories, event_date)
            if candidates_score <= best_score:
                best_score = candidates_score
                best_i = i
                best_j = j

    if best_score < initial_score:

        parked_sailor = crews[-2]["sailors"][best_i].copy()
        crews[-2]["sailors"].pop(best_i)
        crews[-2]["sailors"].insert(best_i, crews[-1]["sailors"][best_j])
        crews[-1]["sailors"].pop(best_j)
        crews[-1]["sailors"].insert(best_j, parked_sailor)

        for crew in crews:
            crew["crew score"] = crew_score(crew, sailor_histories, event_date)

    crews = order_crews_by_score(crews)

    return crews
