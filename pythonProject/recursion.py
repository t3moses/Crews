
import constants
import database

def swaps_from(first_crew, flotilla):

    # return a list of all pairs of sailors such that
    # the first is a member of first_crew
    # the second is a member of another crew in the flotilla

    pair = ["",""]
    swaps = []

    for second_crew in flotilla:
        if second_crew == first_crew:
            continue
        for first_sailor in first_crew["sailors"]:
            for second_sailor in second_crew["sailors"]:
                pair[0] = first_sailor
                pair[1] = second_sailor
                swaps.append(pair)
    return swaps


def swap_flotilla(flotilla, pair):

    # return a copy of flotilla in which the sailors identified by swap have been swapped

    first_crew = [crew for crew in flotilla if not crew["sailors"].count(pair[0]) == 0][0]
    second_crew = [crew for crew in flotilla if not crew["sailors"].count(pair[1]) == 0][0]

    flotilla.remove(first_crew)
    flotilla.remove(second_crew)

    first_crew["sailors"].remove(pair[0])
    second_crew["sailors"].remove(pair[1])

    first_crew["sailors"].append(pair[1])
    second_crew["sailors"].append(pair[0])

    flotilla.append(first_crew)
    flotilla.append(second_crew)

    return flotilla


def complies_with_rule_assist(crew):

    # if the boat in the crew has no assist requirement, or
    # any sailor in the crew has an experienced skill level,
    # return "compliant".  Otherwise, return "non_compliant".

    # database.debug += "assist\n"

    assist = [boat["assistance"] for boat in database.boats_data if boat["key"] == crew["boat"]][0]
    if assist == "False":
        return "compliant"
    for flotilla_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == flotilla_sailor][0]
        if skill == 2:
            return "compliant"
    return "non_compliant"


def complies_with_rule_whitelist(crew):

    # database.debug += "whitelist\n"

    for flotilla_sailor in crew["sailors"]:
        whitelist = [sailor["whitelist"] for sailor in database.sailors_data if sailor["key"] == flotilla_sailor][0]
        if not whitelist.count(crew["boat"]) == 0:
            return "non_compliant"
    return "compliant"


def complies_with_rule_skill(crew):

    # database.debug += "skill\n"

    min_skill = 2
    max_skill = 0
    for flotilla_sailor in crew["sailors"]:
        skill = [sailor["skill"] for sailor in database.sailors_data if sailor["key"] == flotilla_sailor][0]
        min_skill = min(int(skill), min_skill)
        max_skill = min(int(skill), max_skill)
    if max_skill - min_skill < 2:
        return "compliant"
    return "non_compliant"

def complies_with_rule_partner(crew):

    # database.debug += "partner\n"

    for i in range(len(crew["sailors"])):
        for j in range(i + 1, len(crew["sailors"])):
            first_partner = [sailor["partner key"] for sailor in database.sailors_data if sailor["key"] == crew["sailors"][i]][0]
            second_key = [sailor["key"] for sailor in database.sailors_data if sailor["key"] == crew["sailors"][j]][0]
            if first_partner == second_key:
                return "non_compliant"
    return "compliant"


def complies_with_rule_repeat(crew, event_date):

    # database.debug += "repeat\n"

    for sailor in crew["sailors"]:
        sailor_history = [history for history in database.sailor_histories if history["key"] == sailor][0]
        event_index = constants.event_dates.index(event_date)
        for index in (max(0, event_index - constants.streak), max(0, event_index - 1)):
            if sailor_history[constants.event_dates[index]] == crew["boat"]:
                return "non_compliant"
    return "compliant"


def complies_with_rule(crew, rule, event_date):

    # return true if the crew complies with the identified rule.  Otherwise, return false

    match rule:
        case "assist":
            return complies_with_rule_assist(crew)
        case "whitelist":
            return complies_with_rule_whitelist(crew)
        case "skill":
            return complies_with_rule_skill(crew)
        case "partner":
            return complies_with_rule_partner(crew)
        case "repeat":
            return complies_with_rule_repeat(crew, event_date)
    return


def complies(flotilla, rules, event_date):

    database.debug += "\n"

    for crew in flotilla:
        database.debug += str(crew) + "\n"
    database.debug += str(rules) + "\n"

    swaps = []

    while True:
        for crew in flotilla:
            # get the list of eligible swaps between this crew and the rest of the flotilla
            swaps = swaps_from(crew, flotilla)
            for rule in rules:
                if complies_with_rule(crew, rule, event_date) == "non_compliant":

                    # arrive here if the flotilla does not comply with a rule at this depth or above

                    flotilla = swap_flotilla(flotilla, swaps[0]) # try the next swap
                    swaps.pop(0)
                    if len(swaps) == 0:
                        database.debug += "1\n"
                        # return non-compliant if there isn't another flotilla to try
                        return {"status": "non-compliant", "flotilla": flotilla}
                    else: continue
                else: continue # test all crews against all rules

        # arrive here if all crews in the swapped flotilla comply with all rules at this depth and above
        # now try the next level down

        database.debug += "2\n"
        if len(rules) == len(constants.rules):
            database.debug += "3\n"
            # there are no further depths to the rules tree
            return {"status": "compliant", "flotilla": flotilla}
        else:
            # there are one or more further depths to the rules tree
            rules.append(constants.rules[len(rules)]) # add the next rule
            compliance = complies(flotilla, rules, event_date) # RECURSION
            status = compliance["status"]
            if status == "compliant":
                database.debug += "4\n"
                return compliance
            else:
                # try the next flotilla NOT THE ONE THAT WAS RETURNED
                flotilla = swap_flotilla(flotilla, swaps[0])
                swaps.pop(0)
                if len(swaps) == 0:
                    database.debug += "5\n"
                    # return non-compliant if there isn't another flotilla to try
                    return {status, flotilla}
                else:
                    database.debug += "6\n"


# def discretionary(flotilla, event_date):

event_date = "Fri Jul 4"
flotilla = [{"boat": "nina", "sailors": ["joshuaslocum", "timmoses"]},{"boat": "saogabriel", "sailors": ["elizabethcook", "deecaffari"]}, {"boat": "victoria", "sailors": ["sarabramall", "williambligh"]}]
rules = [constants.rules[0]]

database.begin()

compliance = complies(flotilla, rules, event_date)
flotilla = compliance["flotilla"].copy

database.end()

#    return flotilla
