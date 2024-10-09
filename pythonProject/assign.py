import random
import datetime

def assign(available_boats, available_sailors):

    random.seed(42)

    ordered_sailors = order_sailors_by_loyalty(available_sailors)
    ordered_boats = order_boats_by_loyalty(available_boats)

#    crews = [] # list of crew, crew is a list of exactly one boat and one or more sailors.

    min_occupancy = 0
    max_occupancy = 0
    for boat in available_boats:
        min_occupancy += int(boat['min_occupancy'])
        max_occupancy += int(boat['max_occupancy'])

    if len(ordered_sailors) < min_occupancy:
        crews = case_1(ordered_boats, ordered_sailors)
    elif len(ordered_sailors) > max_occupancy:
        crews = case_2(ordered_boats, ordered_sailors)
    else: # len(ordered_sailors) >= min_occupancy AND len(ordered_sailors) <= max_occupancy
        crews = case_3(ordered_boats, ordered_sailors)

    return crews

def case_1(boats, sailors):

    # The number of sailors is less than the minimum number required.
    # remove boats until the minimum number of sailors required is greater than
    # or equal to the number of sailors.

    min_overall = 0
    for boat in boats:
        min_overall += int(boat["min_occupancy"])

    while len(sailors) < min_overall:
        min_overall -= int(boats[-1]["min_occupancy"])
        boats.pop()

    crews = case_3(boats, sailors)
        
    return crews

def case_2(boats, sailors):

    # The number of sailors is greater than the maximum number of spaces available.

    # remove sailors until the number of sailors is equal to max_occupancy.

    max_overall = 0
    for boat in boats:
        max_overall += int(boat["max_occupancy"])

    crews = case_3(boats, sailors[0, max_overall])

    return crews

def case_3(boats, sailors):

    # The number of sailors is greater than or equal to min_occupancy AND
    # The number of sailors is less than or equal to max_occupancy.

    # Set the occupancy of each boat.  Start with min_occupancy.
    # Order the boats by headroom.  For the boat with the greatest headroom, increment
    # the occupancy by 1.  Repeat ordering and incrementing until overall_occupancy
    # is equal to the number of sailors.
    # Reorder boats by loyalty, then assign boats and sailors to crews by loyalty
    # until the number of sailors assigned to each boat is equal to its occupancy.

    min_overall = 0
    max_overall = 0
    for boat in boats:
        boat["occupancy"] = boat["min_occupancy"]
        min_overall += int(boat["min_occupancy"])
        max_overall += int(boat["max_occupancy"])

    if not ( len(sailors) >= min_overall ):
        raise Exception("Number of sailors is less than min_occupancy.")

    if not ( len(sailors) <= max_overall ):
        raise Exception("Number of sailors is greater than max_occupancy.")

    overall_occupancy = min_overall

    while len(sailors) > overall_occupancy:
        boats = order_boats_by_headroom(boats)
        boats[-1]["occupancy"] = str(int(boats[-1]["occupancy"]) + 1)
        overall_occupancy += 1

    crews = allocate(boats, sailors)

    for crew in crews:
        print(crew)

    return crews

def allocate(boats, sailors):

    crews = []
    sailor_number = 0

    for boat in boats:
        crew = []
        crew.append(boat["name"])
        for _ in range(int(boat["occupancy"])):
            crew.append(sailors[sailor_number]["name"])
            sailor_number += 1
        crews.append(crew)

    return crews

def order_sailors_by_loyalty(sailors):

    # create a list that orders sailors by their membership status and loyalty band.
    # the order of sailors in the same loyalty band is randomized.

    members = []
    non_members = []
    ordered_members = []
    ordered_non_members = []
    ordered_sailors = []

    # Divide sailors into members and non-members.

    for sailor in sailors:
        if sailor["member"] == "True":
            members.append(sailor)
        else:
            non_members.append(sailor)

    # order members and non-members into lists of sailors with identical loyalty levels.

    i = len(members)
    loyalty = 0
    while i > 0:
        loyal_members = [] # list of members with the same loyalty level
        for member in members:
            if int(member["loyalty"]) == loyalty:
                loyal_members.append(member)
                i -= 1
        loyalty += 1
        ordered_members.append(loyal_members)

    i = len(non_members)
    loyalty = 0
    while i > 0:
        loyal_non_members = []
        for non_member in non_members:
            if int(non_member["loyalty"]) == loyalty:
                loyal_non_members.append(non_member)
                i -= 1
        loyalty += 1
        ordered_non_members.append(loyal_non_members)

    # For members first and then for non-members, randomize the order within each loyalty level.
    # ordered_sailors will then contain the list of sailors in priority order.
    # First, members are prioritized over non-members.
    # Then those with low loyalty levels are prioritized over those with higher loyalty levels.

    while len(ordered_members) > 0:
        loyal_members = ordered_members[0]
        while len(loyal_members) > 0:
            if len(loyal_members) > 1:
                loyal_member_number = random.randint(0, len(loyal_members) - 1)
            else:
                loyal_member_number = 0
            ordered_sailors.append(loyal_members[loyal_member_number])
            del loyal_members[loyal_member_number]
        del ordered_members[0]

    while len(ordered_non_members) > 0:
        loyal_members = ordered_non_members[0]
        while len(loyal_non_members) > 0:
            if len(loyal_non_members) > 1:
                loyal_non_member_number = random.randint(0, len(loyal_non_members) - 1)
            else:
                loyal_non_member_number = 0
            ordered_sailors.append(loyal_non_members[loyal_non_member_number])
            del loyal_non_members[loyal_non_member_number]
        del ordered_non_members[0]

    for i in range(len(ordered_sailors)):
        print(ordered_sailors[i])
    print()

    return ordered_sailors


def order_boats_by_loyalty(boats):

    # create a list that orders boats by their loyalty band.
    # the order of boats in the same loyalty band is randomized.

    ordered_boats = []
    banded_boats = []

    i = len(boats)
    loyalty = 0
    while i > 0:
        loyal_boats = [] # list of boats in the same loyalty band
        for boat in boats:
            if int(boat["loyalty"]) == loyalty:
                loyal_boats.append(boat)
                i -= 1
        loyalty += 1
        banded_boats.append(loyal_boats)

    while len(banded_boats) > 0:
        while len(banded_boats[0]) > 0:
            if len(banded_boats[0]) > 1:
                banded_boat_number = random.randint(0, len(banded_boats[0]) - 1)
            else:
                banded_boat_number = 0
            ordered_boats.append(banded_boats[0][banded_boat_number])
            del banded_boats[0][banded_boat_number]
        del banded_boats[0]

    return ordered_boats


def order_boats_by_headroom(boats):

    # create a list that orders boats by their headroom band.
    # a boat's headroom is the difference between its max_occupancy and its assigned occupancy.
    # the order of boats in the same headroom band is randomized.

    ordered_boats = []
    banded_boats = []

    i = len(boats)
    headroom = 0
    while i > 0:
        headroom_boats = [] # list of boats in the same headroom band
        for boat in boats:
            if int(boat["max_occupancy"]) - int(boat["occupancy"]) == headroom:
                headroom_boats.append(boat)
                i -= 1
        headroom += 1
        banded_boats.append(headroom_boats)

    while len(banded_boats) > 0:
        while len(banded_boats[0]) > 0:
            if len(banded_boats[0]) > 1:
                banded_boat_number = random.randint(0, len(banded_boats[0]) - 1)
            else:
                banded_boat_number = 0
            ordered_boats.append(banded_boats[0][banded_boat_number])
            del banded_boats[0][banded_boat_number]
        del banded_boats[0]

    return ordered_boats
