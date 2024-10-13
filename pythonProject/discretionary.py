
import random
import constants

def discretionary(crews, sailor_histories, event_date):

    # Add the crew non-compliance score for each crew.

    for crew in crews:

        whitelist_score = constants.whitelist_weight * whitelist(crew)
        partner_score = constants.partner_weight * partner(crew)
        assist_score = constants.assist_weight * assist(crew)
        skill_score = constants.skill_weight * skill(crew)
        repeat_score = constants.repeat_weight * repeat(crew, sailor_histories, event_date)

        crew["score"] = whitelist_score + partner_score + assist_score + skill_score + repeat_score

    return crews

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
                score += history_list.count(crew["boat"]["name"])

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
