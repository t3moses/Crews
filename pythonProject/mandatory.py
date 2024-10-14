import random
import datetime

def mandatory(available_boats, available_sailors):

    # random.seed(42)
    random.seed(str(datetime.datetime.now))

    ordered_sailors = order_sailors_by_loyalty(available_sailors)
    ordered_boats = order_boats_by_loyalty(available_boats)

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
    # Remove boats until the minimum number of sailors required is greater than
    # or equal to the number of sailors.
    # Then apply case 3.

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

    # Remove sailors until the number of sailors is equal to max_occupancy.
    # Then apply case 3.

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

    # Repeatedly add 1 to the occupancy of the boat with the greatest headroom,
    # until overall_occupancy is equal to the number of sailors.

    while len(sailors) > overall_occupancy:
        boats = order_boats_by_headroom(boats)
        boats[-1]["occupancy"] = str(int(boats[-1]["occupancy"]) + 1)
        overall_occupancy += 1

    crews = assign(boats, sailors)

    return crews

def assign(boats, sailors):

    # assign individual sailors to individual boats in loyalty order of both sailors and boats.

    crews = [] # list of crews.
    initial = 0

    boats = order_boats_by_loyalty(boats)

    for boat in boats:
        crew = {}
        crew["boat"] = boat
        final = initial + int(boat["occupancy"])
        crew["sailors"] = sailors[initial : final]
        initial = final
        crews.append(crew)

    return crews

def order_sailors_by_loyalty(sailors):

    # Create a list that orders sailors by their membership status and loyalty band.
    # The order of sailors in the same loyalty band is randomized.

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

    # Order members and non-members into lists of sailors in the same loyalty band.

    i = len(members)
    loyalty = 0
    while i > 0:
        loyal_members = [] # list of members in the same loyalty band.
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

    # For members first and then for non-members, randomize the order within each loyalty band.
    # Ordered_sailors will then contain the list of sailors in priority order.
    # First, members are prioritized over non-members.
    # Then those in low loyalty bands are prioritized over those in higher bands.

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

    return ordered_sailors


def order_boats_by_loyalty(boats):

    # Create a list that orders boats by their loyalty band.
    # The order of boats in the same loyalty band is randomized.

    ordered_boats = []
    banded_boats = []

    i = len(boats)
    loyalty = 0
    while i > 0:
        loyal_boats = [] # list of boats in the same loyalty band.
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

    # Create a list that orders boats by their headroom band.
    # A boat's headroom is the difference between its max_occupancy and its assigned occupancy.
    # The order of boats in the same headroom band is randomized.

    ordered_boats = []
    banded_boats = []

    i = len(boats)
    headroom = 0
    while i > 0:
        headroom_boats = [] # list of boats in the same headroom band.
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
