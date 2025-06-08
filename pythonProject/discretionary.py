
import constants
import database
import copy
import random


def swap_crews(crews, first_sailor, second_sailor):

    # identify the two crews that contain the first_sailor and second_sailor
    # return a list of the crews in which the first_sailor and second_sailor have been swapped

    swapped_crews = []

    first_crew = [crew for crew in crews if crew["sailors"].count(first_sailor) > 0][0]
    second_crew = [crew for crew in crews if crew["sailors"].count(second_sailor) > 0][0]

    index = first_crew["sailors"].index(first_sailor)
    first_crew["sailors"].pop(index)
    first_crew["sailors"].insert(index, second_sailor)

    index = second_crew["sailors"].index(second_sailor)
    second_crew["sailors"].pop(index)
    second_crew["sailors"].insert(index, first_sailor)

    swapped_crews.append(first_crew)
    swapped_crews.append(second_crew)

    return swapped_crews


def swap_events(event, first_sailor, second_sailor):

    # find first_crew, containing first_sailor and second_crew, containing second_sailor
    # replace first_sailor by second_sailor and second_sailor by first_sailor
    # return the event with the swapped crews

    swapped_event = copy.deepcopy(event)
    crews = swapped_event["flotilla"]
    first_crew = [crew for crew in crews if crew["sailors"].count(first_sailor) > 0][0]
    first_crew_index = crews.index(first_crew)

    second_crew = [crew for crew in crews if crew["sailors"].count(second_sailor) > 0][0]
    second_crew_index = crews.index(second_crew)

    sailor_index = first_crew["sailors"].index(first_sailor)
    first_crew["sailors"].pop(sailor_index)
    first_crew["sailors"].insert(sailor_index, second_sailor)

    sailor_index = second_crew["sailors"].index(second_sailor)
    second_crew["sailors"].pop(sailor_index)
    second_crew["sailors"].insert(sailor_index, first_sailor)

    # swap the crews in the event

    swapped_event["flotilla"].pop(first_crew_index)
    swapped_event["flotilla"].insert(first_crew_index, first_crew)

    swapped_event["flotilla"].pop(second_crew_index)
    swapped_event["flotilla"].insert(second_crew_index, second_crew)

    return swapped_event

def assist_score(crew):

    # if the boat in the crew has no assist requirement, or
    # any sailor in the crew has an experienced skill level,
    # return 0.  Otherwise, return assist_weight

    assist = [boat["assistance"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
    if assist.upper() == "FALSE":
        return 0
    for event_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        if int(skill) == 2:
            return 0
    return constants.assist_weight


def whitelist_score(crew):

    for event_sailor in crew["sailors"]:
        whitelist = [sailor["whitelist"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        if whitelist.count(crew["boat"]) == 0:
            return constants.whitelist_weight
        else:
            continue
    return 0


def skill_score(crew):

    min_skill = 2
    max_skill = 0
    for event_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        min_skill = min(int(skill), min_skill)
        max_skill = max(int(skill), max_skill)
    if max_skill - min_skill < 2:
        return 0
    return constants.skill_weight

def partner_score(crew):

    for i in range(len(crew["sailors"])):
        for j in range(len(crew["sailors"])):
            if not i == j:
                first_partner = [sailor["partner key"] for sailor in database.sailors_data if sailor["key"] == crew["sailors"][i]][0]
                second_key = crew["sailors"][j]
                if first_partner == second_key:
                    return constants.partner_weight
    return 0


def repeat_score(crew, event_id):

    for sailor in crew["sailors"]:
        sailor_history = [history for history in database.sailor_histories if history["key"] == sailor][0]
        event_index = constants.event_ids.index(event_id)
        for index in (max(0, event_index - constants.streak), max(0, event_index - 1)):
            if sailor_history[constants.event_ids[index]] == crew["boat"]:
                return constants.repeat_weight
    return 0


def score_from_crew(event, crew):

    # return the overall non-compliance score for the crew

    crew_score = 0
    crew_score += assist_score(crew)
    crew_score += whitelist_score(crew)
    crew_score += skill_score(crew)
    crew_score += partner_score(crew)
    crew_score += repeat_score(crew, event["date"])
    return crew_score


def explanation_from_event(event):

    explanation = ""

    for crew in event["flotilla"]:
        score = score_from_crew(event, crew)
        if score > 0:
            explanation += crew["boat"] + " ("
            if assist_score(crew) > 0:
                explanation += "assist, "
            if whitelist_score(crew) > 0:
                explanation += "whitelist, "
            if skill_score(crew) > 0:
                explanation += "skill, "
            if partner_score(crew) > 0:
                explanation += "partner, "
            if repeat_score(crew, event["date"]) > 0:
                explanation += "repeat, "
            explanation = explanation.rstrip(", ")
            explanation += "), "
    explanation = explanation.rstrip(", ")
    return explanation


def score_from_event(event):

    # return the overall non-compliance score for the event

    event_score = 0
    for crew in event["flotilla"]:
        event_score += score_from_crew(event, crew)
    return event_score


def local_minimum(event):

    # Find a local minimum of the event non-compliance score
    # for the set number of local epochs
    # make a list of crew scores and an overall score for the event
    # if the score for the whole event is 0, return without updating the event
    # find the crew with the highest score
    # posit swaps between the sailors in that crew and all the remaining sailors
    # calculate the score for each posited event
    # if the posited score is less than the event score, update the event with the posited event
    # return the event with the lowest score

    record = {}
    event_score = score_from_event(event)
    if event_score == 0:
        return event

    local_event = copy.deepcopy(event)

    for _ in range(constants.local_epochs):
        crews = event["flotilla"]
        crew_scores = []
        for crew in crews:
            crew_score = score_from_crew(event, crew)
            crew_scores.append(crew_score)
        high_score = 0
        for i in range(len(crew_scores)):
            if crew_scores[i] >= high_score:
                high_score_crew_index = i
                high_score = crew_scores[i]
        high_score_crew = crews[high_score_crew_index]
        for sailor in high_score_crew["sailors"]:
            remaining_crews = copy.deepcopy(crews)
            remaining_crews.pop(high_score_crew_index)
            for remaining_crew in remaining_crews:
                for remaining_sailor in remaining_crew["sailors"]:
                    posit_event = swap_events(event, sailor, remaining_sailor)
                    posit_event_score = score_from_event(posit_event)
                    swapped = False
                    if posit_event_score < event_score:
                        record["interim"] = str(posit_event_score)
                        database.debug.append(record)
                        event_score = posit_event_score
                        local_event = copy.deepcopy(posit_event)
                        if event_score == 0:
                            return local_event
                        else: # next epoch
                            swapped = True
                            break
                if swapped == True:
                    break
            if swapped == True:
                break
    return local_event


def discretionary(event):

    # use gradient descent to find a local minimum
    # if the result is fully compliant, stop
    # shuffle the sailors and try again
    # keep the event with the best score, and
    # if no compliant solution is found, return the one with the best score

    event_score = score_from_event(event)
    if event_score == 0:
        record = {}
        record["final"] = "0"
        database.debug.append(record)
        return event

    local_event = copy.deepcopy(event)
    best_event = local_event

    for _ in range(constants.global_epochs):

        posit_event = local_minimum(local_event)
        posit_event_score = score_from_event(posit_event)
        if posit_event_score == 0:
            record = {}
            record["final"] = "0"
            database.debug.append(record)
            return posit_event
        if posit_event_score < event_score:
            event_score = posit_event_score
            best_event = copy.deepcopy(posit_event)

        # shuffle sailors

        sailor_list = []
        for crew in local_event["flotilla"]:
            sailor_list.extend(crew["sailors"])
        random.shuffle(sailor_list)
        for crew in local_event["flotilla"]:
            for i in range(len(crew["sailors"])):
                crew["sailors"].pop(i)
                crew["sailors"].insert(i, sailor_list[0])
                sailor_list.pop(0)

    best_score = score_from_event(best_event)
    record = {}
    record["final"] = str(best_score)
    record["explanation"] = explanation_from_event(best_event)
    database.debug.append(record)

    return best_event
