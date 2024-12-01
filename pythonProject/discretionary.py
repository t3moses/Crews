
import random
import copy
import constants

def discretionary(flotilla, sailor_histories, event_date):

    # Add the crew non-compliance score for each crew to its dictionary.
    # Calculate the overall non-compliance score for the flotilla.
    # Order the flotilla crews by increasing non-compliance score and call swap.
    # Repeat multiple times and calculate the resulting flotilla score.

    for crew in flotilla["crews"]:

        crew["score"] = crew_score(crew, sailor_histories, event_date)

    flotilla = order_flotilla_by_score(flotilla)

    for _ in range(constants.inner_epochs):
        score = 0
        for crew in flotilla["crews"]:
            score += int(crew["score"])

        best_flotilla = swap(flotilla, sailor_histories, event_date)
   
    best_flotilla["score"] = str(score)

    return best_flotilla

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

    score = 0

    boat_key = crew["boat"]["key"]
    for sailor in crew["sailors"]:
        whitelist = sailor["whitelist"]
        if whitelist.count(boat_key) == 0:
            score += 1

    return score

def partner(crew):

    # Count the number of times a sailor is sailing with their partner.

    score = 0

    for sailor_1 in crew["sailors"]:
        for sailor_2 in crew["sailors"]:
            if sailor_1["partner key"] == sailor_2["key"]:
                score += 1

    return score

def assist(crew):

    # Identify if a boat requiring assistance does not have a sailor with skill level 2.

    if crew["boat"]["assistance"] == "True":
        score = 1

        for sailor in crew["sailors"]:
            if int(sailor["skill"]) == 2:
                score = 0
    else:
        score = 0

    return score

def skill(crew):

    # Identify if the spread of skill levels on the boat is greater than 1.

    max_skill = 0
    min_skill = 2

    for sailor in crew["sailors"]:
        max_skill = max( int(sailor["skill"]), max_skill)
        min_skill = min( int(sailor["skill"]), min_skill)
    spread = max_skill - min_skill
    if spread > 1:
        score = 1
    else:
        score = 0

    return score

def repeat(crew, sailor_histories, event_date):

    # Calculate a score based on how recently each sailor has sailed on the current boat.

    score = 0
    for sailor in crew["sailors"]:
        for sailor_history in sailor_histories:
            if sailor_history["key"] == sailor["key"]:
                for date in constants.event_dates:
                    if date == event_date:
                        break
                    else:
                        if sailor_history[date] == crew["boat"]["key"]:
                            contribution = pow(constants.event_dates.index(event_date) - constants.event_dates.index(date), constants.repeat_exponent)
                            score += contribution
    return int(score) # The above calculation results in a float.


def order_flotilla_by_score(flotilla):

    # Create a list that orders flotilla crews by their non-compliance score.
    # The order of crews in the same score band is randomized.

    ordered_crews = []
    banded_crews = []

    i = len(flotilla["crews"])
    score = 0
    while i > 0:
        equal_crews = [] # list of crews in the same score band.
        for crew in flotilla["crews"]:
            if int(crew["score"]) == score:
                equal_crews.append(crew)
                i -= 1
        score += 1
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

    flotilla["crews"] = ordered_crews

    return flotilla

def swaps(flotilla, sailor_histories, event_date):

    for _ in range(5):

        flotilla = swap(flotilla, sailor_histories, event_date)

    return flotilla

def swap(flotilla, sailor_histories, event_date):

    # The received flotilla crews contains a list of crew in increasing non-compliance order.
    # Hence, the last two entries have the highest non-compliance scores.
    # Calculate the initial non-compliance score for the flotilla.
    # From flotilla, select the two crews with the highest non-compliance scores.
    # Swap a pair of sailors between these two flotillas.
    # Calculate the new non-compliance score.
    # Repeat for each pair of sailors, recording the resulting non-compliance scores.
    # If the best swap is not worse than the original, update flotilla.

    global best_i, best_j

    if len(flotilla["crews"]) < 2:
        for crew in flotilla["crews"]:
            crew["score"] = crew_score(crew, sailor_histories, event_date)

        flotilla["score"] = 0
        for crew in flotilla["crews"]:
            flotilla["score"] += crew["score"]

        return flotilla

    initial_score = 0
    for crew in flotilla["crews"]:
        initial_score += crew["score"]
    best_score = initial_score

    for i in range(len(flotilla["crews"][-2]["sailors"])):
        for j in range(len(flotilla["crews"][-1]["sailors"])):
            candidates = copy.deepcopy(flotilla)

            parked_sailor = candidates["crews"][-2]["sailors"][i].copy()
            candidates["crews"][-2]["sailors"].pop(i)
            candidates["crews"][-2]["sailors"].insert(i, candidates["crews"][-1]["sailors"][j])
            candidates["crews"][-1]["sailors"].pop(j)
            candidates["crews"][-1]["sailors"].insert(j, parked_sailor)

            candidates_score = 0
            for candidate in candidates["crews"]:
                candidates_score += crew_score(candidate, sailor_histories, event_date)
            if candidates_score <= best_score:
                best_score = candidates_score
                best_i = i
                best_j = j

    if best_score < initial_score:

        parked_sailor = flotilla["crews"][-2]["sailors"][best_i].copy()
        flotilla["crews"][-2]["sailors"].pop(best_i)
        flotilla["crews"][-2]["sailors"].insert(best_i, flotilla["crews"][-1]["sailors"][best_j])
        flotilla["crews"][-1]["sailors"].pop(best_j)
        flotilla["crews"][-1]["sailors"].insert(best_j, parked_sailor)

        for crew in flotilla["crews"]:
            crew["score"] = crew_score(crew, sailor_histories, event_date)

    flotilla["score"] = 0
    for crew in flotilla["crews"]:
        flotilla["score"] += crew["score"]

    flotilla = order_flotilla_by_score(flotilla)

    return flotilla
