
import database
import random
import copy
import constants

def discretionary(flotilla, event_date):

    # Mandatory policy enforcement does not supply a non-compliance score.  So, add one here.
    # Order the flotilla crews by increasing non-compliance score and call swap.
    # Repeat multiple times starting each pass with the best result from the previous pass.

    flotilla = add_score_to_flotilla(flotilla, event_date)
    flotilla = order_flotilla_by_score(flotilla)
    debug_from_flotilla(flotilla)
    database.debug += "initial flotilla score: " + flotilla["score"] + "\n\n\n"

    for iteration in range(constants.inner_epochs):

        if iteration == 0:
            best_flotilla = copy.deepcopy(flotilla)
        else:
            candidate_flotilla = swap(best_flotilla, event_date)
            if int(candidate_flotilla["score"]) < int(best_flotilla["score"]):
                best_flotilla = copy.deepcopy(candidate_flotilla)

            database.debug += "best flotilla score: " + best_flotilla["score"] + "\n\n\n"

    return best_flotilla

def debug_from_flotilla(flotilla):

    # Write flotilla details to the debug file.

    for crew in flotilla["crews"]:
        database.debug += crew["boat"]["display name"] + " "
        for sailor in crew["sailors"]:
            database.debug += sailor["display name"] + " "
        database.debug += crew["score"] + "\n"
    database.debug += "flotilla score: " + flotilla["score"] + "\n\n"
    return

def add_score_to_flotilla(flotilla, event_date):

    # Fill the flotilla's non-compliance score and the flotilla's crews' non-compliance scores.

    flotilla_score = 0
    for crew in flotilla["crews"]:
        crew_score = score_from_crew(crew, event_date)
        crew["score"] = str(crew_score) 
        flotilla_score += crew_score
    flotilla["score"] = str(flotilla_score)
    return flotilla

def score_from_crew(crew, event_date):

    # Calculate the non-compliance score for one crew.

    whitelist_score = constants.whitelist_weight * whitelist(crew)
    partner_score = constants.partner_weight * partner(crew)
    assist_score = constants.assist_weight * assist(crew)
    skill_score = constants.skill_weight * skill(crew)
    repeat_score = int(float(constants.repeat_weight) * repeat(crew, event_date))

    crew_score = whitelist_score + partner_score + assist_score + skill_score + repeat_score

    return crew_score # Integer.

def whitelist(crew):

    # Count the number of times the boat is not on one of its crew's whitelist.

    score = 0

    boat_key = crew["boat"]["key"]
    for sailor in crew["sailors"]:
        whitelist = sailor["whitelist"]
        if whitelist.count(boat_key) == 0: # The boat is not on the sailor's whitelist.
            score += 1

    return score # Integer.

def partner(crew):

    # Count the number of times a sailor is sailing with their partner.

    score = 0

    for sailor_1 in crew["sailors"]:
        for sailor_2 in crew["sailors"]:
            if sailor_1["partner key"] == sailor_2["key"]:
                score += 1

    return score # Integer.

def assist(crew):

    # Identify if a boat requiring assistance does not have a sailor with skill level 2.

    if crew["boat"]["assistance"] == "True":
        score = 1

        for sailor in crew["sailors"]:
            if int(sailor["skill"]) == 2:
                score = 0
                break
    else:
        score = 0

    return score # Integer.

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

    return score # Integer.

def repeat(crew, event_date):

    # Calculate a score based on how recently each sailor has sailed on the current boat.

    score = 0.0
    for sailor in crew["sailors"]:
        for sailor_history in database.sailor_histories:
            if sailor_history["key"] == sailor["key"]:
                for date in constants.event_dates:
                    if date == event_date:
                        break
                    else:
                        if sailor_history[date] == crew["boat"]["key"]:
                            contribution = pow(float(constants.event_dates.index(event_date) - constants.event_dates.index(date)), constants.repeat_exponent)
                            score += contribution
    return score # Float.

def order_flotilla_by_score(flotilla):

    # Create a flotilla that orders its crews by their non-compliance score.
    # banded_crews is a list of lists of crews, in which the inner list represents crews
    # with the same non-compliance score.
    # The order of crews in the same non-compliance band is randomized.
    # The outer list contains all crews in the flotilla, in ascending order of non-compliance.
    # In this way, the last two crews represent those with the highest non-compliance scores.

    ordered_crews = []
    banded_crews = []

    i = len(flotilla["crews"])
    score = 0
    while i > 0: # Work through all the crews.
        equal_crews = [] # list of crews in the same non-compliance band.
        for crew in flotilla["crews"]: # Work through all the crews again.
            if int(crew["score"]) == score:
                equal_crews.append(crew)
                i -= 1
        score += 1 # Work through the range of non-compliance scores until all crews have been added.
        banded_crews.append(equal_crews)

    while len(banded_crews) > 0: # 1 or more bob-compliance bands.
        while len(banded_crews[0]) > 0: # There are one or more crews in the band.
            if len(banded_crews[0]) > 1:
                crew_number = random.randint(0, len(banded_crews[0]) - 1)
            else: # Just 1 crew in the band.
                crew_number = 0
            ordered_crews.append(banded_crews[0][crew_number])
            banded_crews[0].pop(crew_number) # Move the crew to the banded_crews list.
        banded_crews.pop(0)

    flotilla["crews"] = copy.deepcopy(ordered_crews)

    return flotilla

def swap(flotilla, event_date):

    # The received flotilla contains a list of crews.
    # But, if there are less than two crews, there is no point making changes.
    # Calculate the initial non-compliance score for the flotilla.
    # Order the crews by increasing non-compliance.
    # Then the last two crews have the highest non-compliance scores.
    # Swap all pairs of sailors between the two least compliant crews.
    # Calculate the non-compliance score for each swap.
    # If the best swap is not worse than the original, update the flotilla.

    global best_i, best_j

    if len(flotilla["crews"]) < 2:
        return flotilla

    # Else ...

    flotilla = order_flotilla_by_score(flotilla)
    best_flotilla = copy.deepcopy(flotilla)

    for i in range(len(flotilla["crews"][-2]["sailors"])):
        for j in range(len(flotilla["crews"][-1]["sailors"])):

            candidate_flotilla = copy.deepcopy(flotilla)
            candidate_flotilla["crews"][-2]["sailors"][i] = flotilla["crews"][-1]["sailors"][j]
            candidate_flotilla["crews"][-1]["sailors"][j] = flotilla["crews"][-2]["sailors"][i]

            candidate_flotilla = add_score_to_flotilla(candidate_flotilla, event_date)
            if int(candidate_flotilla["score"]) <= int(best_flotilla["score"]):
                best_flotilla = copy.deepcopy(candidate_flotilla)
                best_flotilla = add_score_to_flotilla(best_flotilla)

            debug_from_flotilla(best_flotilla)

    return best_flotilla
