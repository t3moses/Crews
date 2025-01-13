
import constants
import database


def swap_sailor(event, first_sailor, second_sailor):

    # identify the two crews that contain the first_sailor and second_sailor
    # return a list of the crews in which the first_sailor and second_sailor have been swapped

    print(first_sailor, second_sailor)

    swapped_crews = []

    first_crew = [crew for crew in event["flotilla"] if crew["sailors"].count(first_sailor) > 0][0]
    second_crew = [crew for crew in event["flotilla"] if crew["sailors"].count(second_sailor) > 0][0]

    print(first_crew, second_crew)

    index = first_crew["sailors"].index(first_sailor)
    first_crew["sailors"].pop(index)
    first_crew["sailors"].insert(index, second_sailor)

    index = second_crew["sailors"].index(second_sailor)
    second_crew["sailors"].pop(index)
    second_crew["sailors"].insert(index, first_sailor)

    swapped_crews.append(first_crew)
    swapped_crews.append(second_crew)

    return swapped_crews


def replace_crew(event, first_crew, second_crew):

    # return an event in which the first_crew has been replaced by the second_crew

    index = event["flotilla"].index(first_crew)
    event["flotilla"].pop(index)
    event["flotilla"].insert(index, second_crew)

    return event

def check_assist(crew):

    # if the boat in the crew has no assist requirement, or
    # any sailor in the crew has an experienced skill level,
    # return "compliant".  Otherwise, return "non-compliant".

    assist = [boat["assistance"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
    if assist == "False":
        # database.debug += "-Y\n"
        return "compliant"
    for event_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        if int(skill) == 2:
            # database.debug += "-Y\n"
            return "compliant"
    # database.debug += "-N\n"
    return "non-compliant"


def check_whitelist(crew):

    for event_sailor in crew["sailors"]:
        whitelist = [sailor["whitelist"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        if whitelist.count(crew["boat"]) == 0:
            # database.debug += "--N\n"
            return "non-compliant"
        else:
            continue
    # database.debug += "--Y\n"
    return "compliant"


def check_skill(crew):

    min_skill = 2
    max_skill = 0
    for event_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == event_sailor][0]
        min_skill = min(int(skill), min_skill)
        max_skill = max(int(skill), max_skill)
    if max_skill - min_skill < 2:
        # database.debug += "---Y\n"
        return "compliant"
    # database.debug += "---N\n"
    return "non-compliant"

def check_partner(crew):

    for i in range(len(crew["sailors"]) - 1):
        for j in range(i + 1, len(crew["sailors"])):
            first_partner = [sailor["partner key"] for sailor in database.sailors_data if sailor["key"] == crew["sailors"][i]][0]
            second_key = [sailor["key"] for sailor in database.sailors_data if sailor["key"] == crew["sailors"][j]][0]
            if first_partner == second_key:
                # database.debug += "----N\n"
                return "non-compliant"
    # database.debug += "----Y\n"
    return "compliant"


def check_repeat(crew, event_date):

    for sailor in crew["sailors"]:
        sailor_history = [history for history in database.sailor_histories if history["key"] == sailor][0]
        event_index = constants.event_dates.index(event_date)
        for index in (max(0, event_index - constants.streak), max(0, event_index - 1)):
            if sailor_history[constants.event_dates[index]] == crew["boat"]:
                # database.debug += "-----N\n"
                return "non-compliant"
    # database.debug += "-----Y\n"
    return "compliant"


def check_compliant(event, crew, rule):

    # return "compliant" if the crew complies with the identified rule.  Otherwise, return "non-compliant"

    match rule:
        case "assist":
            return check_assist(crew)
        case "whitelist":
            return check_whitelist(crew)
        case "skill":
            return check_skill(crew)
        case "partner":
            return check_partner(crew)
        case "repeat":
            return check_repeat(crew, event["date"])
    return


def make_compliant(event, first_crew, rules):

    # first_crew fails to comply with rules[-1]
    # find a swap that makes both crews compliant with all rules
    print()
    swaps = []

    # print(first_crew)
    # print(event["flotilla"])
    flotilla = [crew for crew in event["flotilla"] if not crew == first_crew]
    # print(flotilla)

    # print()
    for first_sailor in first_crew["sailors"]:
        for second_crew in flotilla:
            for second_sailor in second_crew["sailors"]:
                posited_crews = swap_sailor(event, first_sailor, second_sailor)
                swaps.append(posited_crews)

                # print(posited_crews)

    for swap in swaps:
        for rule in rules:
            if check_compliant(event, swap[0], rule) == "compliant" and \
                check_compliant(event, swap[1], rule) == "compliant":
                compliant = "compliant" # try next rule
            else:
                compliant = "non-compliant" # try next swap
                break
        if compliant == "compliant":
            event = replace_crew(event, swap[0], swap[1])
            event = replace_crew(event, swap[1], swap[0])
            return event  # compliant

    return event  # non-compliant


def discretionary(event):

    # for each rule in the list of rules
    # then for each crew in the event
    # check if the crew complies with the rule
    # in case it does not, adjust the event's crews until the crew complies with
    # all rules to the depth of the current rule while ensuring that all other crews
    # also comply

    for i in range(len(constants.rules)):
        for j in range(len(event["flotilla"])):
            crew = event["flotilla"][j]
            rule = constants.rules[i]
            if check_compliant(event, crew, rule) == "compliant":
                continue
            else:
                event = make_compliant(event, crew, constants.rules[:i+1])
    return event
