
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import constants

def discretionary(crews, sailor_histories, event_date):

    # Add the crew non-compliance score for each crew to its dictionary.
    # Calculate the overall non-compliance score for the flotilla.
    # Order the crews by increasing non-compliance score,
    # and call swap.
    # Repeat multiple times and calculate the resulting overall score.

    score_list = []

    for crew in crews:
        crew["score"] = crew_score(crew, sailor_histories, event_date)
    crews = order_crews_by_score(crews)

    for _ in range(11):

        overall_score = 0
        for crew in crews:
            overall_score += crew["score"]
        score_list.append(overall_score)

        crews = swap(crews, sailor_histories, event_date)

    overall_score = 0
    for crew in crews:
        overall_score += crew["score"]
    score_list.append(overall_score)

    plt.plot(np.array(score_list))
    plt.ylabel("Loss")
    plt.show()

    return crews

def crew_score(crew, sailor_histories, event_date):

    # Calculate the non-compliance score for one crew.

    whitelist_score = constants.whitelist_weight * whitelist(crew)
    partner_score = constants.partner_weight * partner(crew)
    assist_score = constants.assist_weight * assist(crew)
    skill_score = constants.skill_weight * skill(crew)
    repeat_score = constants.repeat_weight * repeat(crew, sailor_histories, event_date)

    score = whitelist_score + partner_score + assist_score + skill_score + repeat_score

    return score

def whitelist(crew):

    # Count the number of times the boat is not on a sailor's whitelist.

    score = 0

    boat_name = crew["boat"]["name"]
    for i in range(0, len(crew["sailors"])):
        whitelist = crew["sailors"][i]["whitelist"]
        if whitelist.count(boat_name) == 0:
            score += 1

    return score

def partner(crew):

    # Count the number of times a sailor is sailing with their partner.

    score = 0

    for i in range(0, len(crew["sailors"]) - 1):
        for j in range(i, len(crew["sailors"])):
            if crew["sailors"][i]["partner"] == crew["sailors"][j]["name"]:
                score += 1

    return score

def assist(crew):

    # Identify if a boat requiring assistance does not have a sailor with skill level 2.

    if crew["boat"]["assist"] == "True":
        score = 1

        for i in range(0, len(crew["sailors"])):
            if int(crew["sailors"][i]["skill"]) == 2:
                score = 0
    else:
        score = 0

    return score

def skill(crew):

    # Identify if the spread of skill levels on the boat is greater than 1.

    max_skill = 0
    min_skill = 2

    for i in range(0, len(crew["sailors"])):
        max_skill = max( int(crew["sailors"][i]["skill"]), max_skill)
        min_skill = min( int(crew["sailors"][i]["skill"]), min_skill)
    spread = max_skill - min_skill
    if spread > 1:
        score = 1
    else:
        score = 0

    return score

def repeat(crew, sailor_histories, event_date):

    # Count the number of times in the history that a sailor has been assigned to this boat.

    score = 0
    for i in range(0, len(crew["sailors"])):
        for sailor_history in sailor_histories:
            if sailor_history["name"] == crew["sailors"][i]["name"]:
                history_keys = list(sailor_history.keys())
                event_index = history_keys.index(event_date)
                history_list = list(sailor_history.values())[1 : event_index]
                score += int(pow(history_list.count(crew["boat"]["name"]), constants.repeat_exponent))

    return score


def order_crews_by_score(crews):

    # Create a list that orders crews by their non-compliance score.
    # The order of crews in the same score band is randomized.

    ordered_crews = []
    banded_crews = []

    i = len(crews)
    score = 0
    while i > 0:
        equal_crews = [] # list of boats in the same score band.
        for crew in crews:
            if int(crew["score"]) == score:
                equal_crews.append(crew)
                i -= 1
        score += 1
        banded_crews.append(equal_crews)

    while len(banded_crews) > 0:
        while len(banded_crews[0]) > 0: # There are one or more sailors in the crew.
            if len(banded_crews[0]) > 1:
                banded_boat_number = random.randint(0, len(banded_crews[0]) - 1)
            else:
                banded_boat_number = 0
            ordered_crews.append(banded_crews[0][banded_boat_number])
            del banded_crews[0][banded_boat_number]
        del banded_crews[0]

    return ordered_crews

def swaps(crews, sailor_histories, event_date):

    for _ in range(5):

        crews = swap(crews, sailor_histories, event_date)

    return crews

def swap(crews, sailor_histories, event_date):

    # The received crews list contains a list of crews in increasing non-compliance order.
    # Hence the last two entries have the highest non-compliance scores.
    # Calculate the initial non-compliance score for the flotilla.
    # From crews, select the two crews with the highest non-compliance scores.
    # Swap a pair of sailors between these two crews.
    # Calculate the new non-compliance score.
    # Repeat for each pair of sailors, recording the resulting non-compliance scores.
    # If the best swap is not worse than the original, update crews.

    global best_i, best_j
    initial_score = 0
    for crew in crews:
        initial_score += crew["score"]
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
            crew["score"] = crew_score(crew, sailor_histories, event_date)

    crews = order_crews_by_score(crews)

    return crews
