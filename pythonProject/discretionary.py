
import random
import copy
import constants

def discretionary(flotilla, sailor_histories, event_date):

    # Add the crew non-compliance score for each crew to its dictionary.
    # Calculate the overall non-compliance score for the flotilla.
    # Order the flotilla by increasing non-compliance score and call swap.
    # Repeat multiple times and calculate the resulting overall score.

    for crew in flotilla:

        crew["crew score"] = crew_score(crew, sailor_histories, event_date)

    flotilla = order_flotilla_by_score(flotilla)

    best_flotilla = []

    for _ in range(constants.inner_epochs):
        flotilla_score = 0
        for crew in flotilla:
            flotilla_score += int(crew["crew score"])

        best_flotilla = swap(flotilla, sailor_histories, event_date)

    scored_flotilla = {}
    scored_flotilla["flotilla"] = best_flotilla
    scored_flotilla["flotilla score"] = str(flotilla_score)

    return scored_flotilla

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

    # Count the number of times the boat is not on one of its crew's whitelist.

    crew_score = 0

    boat_key = crew["boat"]["key"]
    for sailor in crew["sailors"]:
        whitelist = sailor["whitelist"]
        if whitelist.count(boat_key) == 0:
            crew_score += 1

    return crew_score

def partner(crew):

    # Count the number of times a sailor is sailing with their partner.

    crew_score = 0

    for sailor_1 in crew["sailors"]:
        for sailor_2 in crew["sailors"]:
            if sailor_1["partner key"] == sailor_2["key"]:
                crew_score += 1

    return crew_score

def assist(crew):

    # Identify if a boat requiring assistance does not have a sailor with skill level 2.

    if crew["boat"]["assistance"] == "True":
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

    # Calculate a score based on how recently each sailor has sailed on the current boat.

    crew_score = 0
    for sailor in crew["sailors"]:
        for sailor_history in sailor_histories:
            if sailor_history["key"] == sailor["key"]:
                for date in constants.event_dates:
                    if date == event_date:
                        break
                    else:
                        if sailor_history[date] == crew["boat"]["key"]:
                            contribution = pow(constants.event_dates.index(event_date) - constants.event_dates.index(date), constants.repeat_exponent)
                            crew_score += contribution
    return int(crew_score) # The above calculation results in a float.


def order_flotilla_by_score(flotilla):

    # Create a list that orders flotilla by their non-compliance score.
    # The order of flotilla in the same score band is randomized.

    ordered_flotilla = []
    banded_flotilla = []

    i = len(flotilla)
    crew_score = 0
    while i > 0:
        equal_flotilla = [] # list of boats in the same score band.
        for crew in flotilla:
            if int(crew["crew score"]) == crew_score:
                equal_flotilla.append(crew)
                i -= 1
        crew_score += 1
        banded_flotilla.append(equal_flotilla)

    while len(banded_flotilla) > 0:
        while len(banded_flotilla[0]) > 0: # There are one or more sailors in the crew.
            if len(banded_flotilla[0]) > 1:
                boat_number = random.randint(0, len(banded_flotilla[0]) - 1)
            else:
                boat_number = 0
            ordered_flotilla.append(banded_flotilla[0][boat_number])
            banded_flotilla[0].pop(boat_number)
        banded_flotilla.pop(0)

    return ordered_flotilla

def swaps(flotilla, sailor_histories, event_date):

    for _ in range(5):

        flotilla = swap(flotilla, sailor_histories, event_date)

    return flotilla

def swap(flotilla, sailor_histories, event_date):

    # The received flotilla list contains a list of flotilla in increasing non-compliance order.
    # Hence, the last two entries have the highest non-compliance scores.
    # Calculate the initial non-compliance score for the flotilla.
    # From flotilla, select the two flotilla with the highest non-compliance scores.
    # Swap a pair of sailors between these two flotilla.
    # Calculate the new non-compliance score.
    # Repeat for each pair of sailors, recording the resulting non-compliance scores.
    # If the best swap is not worse than the original, update flotilla.

    global best_i, best_j
    initial_score = 0
    for crew in flotilla:
        initial_score += crew["crew score"]
    best_score = initial_score

    for i in range (len(flotilla[-2]["sailors"])):
        for j in range (len(flotilla[-1]["sailors"])):
            candidates = copy.deepcopy(flotilla)
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

        parked_sailor = flotilla[-2]["sailors"][best_i].copy()
        flotilla[-2]["sailors"].pop(best_i)
        flotilla[-2]["sailors"].insert(best_i, flotilla[-1]["sailors"][best_j])
        flotilla[-1]["sailors"].pop(best_j)
        flotilla[-1]["sailors"].insert(best_j, parked_sailor)

        for crew in flotilla:
            crew["crew score"] = crew_score(crew, sailor_histories, event_date)

    flotilla = order_flotilla_by_score(flotilla)

    return flotilla
