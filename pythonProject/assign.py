import random
import datetime

def assign(available_boats, available_sailors):

    random.seed(42)

    ordered_sailors = order_sailors(available_sailors)
    ordered_boats = order_boats(available_boats)

#    crews = [] # list of crew, crew is a list of exactly one boat and one or more sailors.

    min_occupancy = 0
    max_occupancy = 0
    for boat in available_boats:
        min_occupancy += int(boat['min_occupancy'])
        max_occupancy += int(boat['max_occupancy'])

    if len(ordered_sailors) < min_occupancy:
        crews = case_1(ordered_boats, ordered_sailors)
    elif len(ordered_sailors) < max_occupancy:
        crews = case_2(ordered_boats, ordered_sailors)
    elif len(ordered_sailors) == max_occupancy:
        crews = case_3(ordered_boats, ordered_sailors)
    else: # len(ordered_sailors) > max_occupancy:
        crews = case_4(ordered_boats, ordered_sailors)

    return crews

def case_1(boats, sailors):

    # The number of sailors is less than the minimum number of spaces.

    min_overall = 0
    for boat in boats:
        min_overall += int(boat["min_occupancy"])

    while len(sailors) < min_overall:
        boat_number = random.randint(0, len(boats) - 1)
        min_overall -= int(boats[boat_number]["min_occupancy"])
        del boats[boat_number]

    for boat in boats:
        boat["occupancy"] = boat["min_occupancy"]

    if len(sailors) > min_overall:
        crews = case_2(boats, sailors)
    else:
        crews = case_3(boats, sailors)
        
    return crews

def case_2(boats, sailors):

    # The number of sailors is less than the maximum number of spaces.

    # initially set each boat occupancy to its maximum capacity.

    overall_capacity = 0
    for boat in boats:
        boat["occupancy"] = boat["max_occupancy"]
        overall_capacity += int(boat["max_occupancy"])
    overall_occupancy = overall_capacity

    # pass through partially_filled_boats repeatedly until overall capacity is equal to the number of sailors.

    iteration = 0
    while overall_occupancy > len(sailors):

        # reduce the occupancy of each boat at random until all boat occupancies have been reduced by 1
        # or overall_occupancy is equal to the number of sailors.

        while overall_capacity - iteration * len(boats) > len(sailors): # repeat until exactly 1 occupancy has been removed from each boat.
            boat_number = random.randint(0, len(boats) - 1)
            if int(boats[boat_number]["occupancy"]) >= int(boats[boat_number]['max_occupancy']) - iteration:
                boats[boat_number]["occupancy"] = str( int(boats[boat_number]["occupancy"]) - 1)
                overall_occupancy -= 1
                if overall_occupancy <= len(sailors):
                    break # out of the closest while loop.

        iteration += 1

    crews = case_3(boats, sailors)

    return crews

def case_3(boats, sailors):

    # The number of sailors is equal to the number of available spaces.

    overall_occupancy = 0
    for boat in boats:
        overall_occupancy += int(boat["occupancy"])

    if not overall_occupancy == len(sailors):
        raise Exception("Number of sailors not equal to overall number of available spaces.")

    crews = []

    while not (len(boats) == 0):
        crew = []
        boat_number = random.randint(0, len(boats) - 1)
        crew.append(boats[boat_number]['name'])
        occupants = 0
        while occupants < int(boats[boat_number]['max_occupancy']):
            if len(sailors) == 0:
                break
            sailor_number = random.randint(0, len(sailors) - 1)
            crew.append(sailors[sailor_number]['name'])
            del sailors[sailor_number]
            occupants += 1
        crews.append(crew)
        del boats[boat_number]

    return crews

def case_4(boats, sailors):
    
    # The number of sailors is greater than the number of available spaces.

    crews = []

    pass
    return crews


def order_sailors(sailors):

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
    # Then those with the lower loyalty levels are prioritized over those with higher loyalty levels.

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


def order_boats(boats):

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

    for i in range(len(ordered_boats)):
        print(ordered_boats[i])
    print()

    return ordered_boats