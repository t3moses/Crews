import constants

def non_compliance(crews, sailor_histories, event_date):

    """

    print()
    print("Whitelist")
    for crew in crews:
        whitelist_score = whitelist(crew)
        print(whitelist_score)
    print()
    print("Partners")
    for crew in crews:
        partner_score = partner(crew)
        print(partner_score)
    print()
    print("Assist")
    for crew in crews:
        assist_score = assist(crew)
        print(assist_score)
    print()
    print("Skill")
    for crew in crews:
        skill_score = skill(crew)
        print(skill_score)
    print()
    print("Repeat")
    for crew in crews:
        repeat_score = repeat(crew, sailor_histories, event_date)
        print(repeat_score)
    print()

    """

    print()
    print("overall score")
    print()
    
    for crew in crews:

        whitelist_score = constants.whitelist_weight * whitelist(crew)
        partner_score = constants.partner_weight * partner(crew)
        assist_score = constants.assist_weight * assist(crew)
        skill_score = constants.skill_weight * skill(crew)
        repeat_score = constants.repeat_weight * repeat(crew, sailor_histories, event_date)

        overall_score = whitelist_score + partner_score + assist_score + skill_score + repeat_score

        print(overall_score)

    print()

    return

def whitelist(crew):

    score = 0

    boat_name = crew[0]["name"]
    for i in range(1, len(crew)):
        whitelist = crew[i]["whitelist"]
        if whitelist.count(boat_name) == 0:
            score += 1

    return score

def partner(crew):

    score = 0

    for i in range(1, len(crew) - 1):
        for j in range(i, len(crew)):
            if crew[i]["partner"] == crew[i + 1]["name"]:
                score += 1

    return score

def assist(crew):

    if crew[0]["assist"] == "True":
        score = 1
        for i in range(1, len(crew)):
            if int(crew[i]["skill"]) == 2:
                score = 0
    else:
        score = 0

    return score

def skill(crew):

    max_skill = 0
    min_skill = 2

    for i in range(1, len(crew)):
        max_skill = max( int(crew[i]["skill"]), max_skill)
        min_skill = min( int(crew[i]["skill"]), min_skill)
    spread = max_skill - min_skill
    if spread > 1:
        score = 1
    else:
        score = 0

    return score

def repeat(crew, sailor_histories, event_date):
    score = 0
    for i in range(1, len(crew)):
        for sailor_history in sailor_histories:
            if sailor_history["name"] == crew[i]["name"]:
                history_keys = list(sailor_history.keys())
                event_index = history_keys.index(event_date)
                history_list = list(sailor_history.values())[1 : event_index]
                score += history_list.count(crew[0]["name"])

    return score
