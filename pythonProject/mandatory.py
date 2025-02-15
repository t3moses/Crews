
import database
import sys
import random

def mandatory(available_boats, available_sailors):

    ordered_sailors = order_sailors_by_loyalty(available_sailors)
    ordered_boats = order_boats_by_loyalty(available_boats)

    min_occupancy = 0
    max_occupancy = 0
    for available_boat in available_boats:
        min_occupancy += [int(boat['min occupancy']) for boat in database.boats_data if boat["key"] == available_boat][0]
        max_occupancy += [int(boat['max occupancy']) for boat in database.boats_data if boat["key"] == available_boat][0]

    if len(ordered_sailors) < min_occupancy:
        extended_flotilla = case_1(ordered_boats, ordered_sailors)
    elif len(ordered_sailors) > max_occupancy:
        extended_flotilla = case_2(ordered_boats, ordered_sailors)
    else: # len(ordered_sailors) >= min_occupancy AND len(ordered_sailors) <= max_occupancy
        extended_flotilla = case_3(ordered_boats, ordered_sailors)

    return extended_flotilla

def case_1(boats, sailors):

    # The number of sailors is less than the minimum number required.
    # Remove boats until the minimum number of sailors required is less than
    # or equal to the number of sailors available.
    # Then apply case 3.

    min_overall = 0
    max_overall = 0
    for event_boat in boats:
        min_overall += [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == event_boat][0]
        max_overall += [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == event_boat][0]

    while len(sailors) < min_overall:
        min_overall -= [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == boats[-1]][0]
        max_overall -= [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == boats[-1]][0]
        boats.pop() # Remove the last boat in the list.

    if len(sailors) > max_overall:
        extended_flotilla = case_2(boats, sailors)
    else:
        extended_flotilla = case_3(boats, sailors)

    return extended_flotilla

def case_2(boats, sailors):

    # The number of sailors is greater than the maximum number of spaces available.
    # Remove sailors until the number of sailors is equal to the maximum number of spaces available.
    # Then apply case 3.  Excess sailors are assigned to the wait list.

    max_overall = 0
    for available_boat in boats:
        max_overall += [int(boat['max occupancy']) for boat in database.boats_data if boat["key"] == available_boat][0]

    extended_flotilla = case_3(boats, sailors[ : max_overall])
    extended_flotilla["wait list"] = sailors[max_overall : ]

    return extended_flotilla

def case_3(event_boats, event_sailors):

    # The number of sailors is greater than or equal to minimum number required AND
    # The number of sailors is less than or equal to the number of spaces available.

    # Set the occupancy of each boat, starting with min_occupancy.
    # Order the boats by headroom.  For the boat with the greatest headroom, increment
    # the occupancy by 1.  Repeat ordering and incrementing until overall_occupancy
    # is equal to the number of sailors.

    min_overall = 0
    max_overall = 0
    for event_boat in event_boats:
        for boat in database.boats_data:
            if event_boat == boat["key"]:
                boat["actual_occupancy"] = boat["min occupancy"]
                min_overall += int(boat["min occupancy"])
                max_overall += int(boat["max occupancy"])

    if len(event_sailors) < min_overall:
        print("Number of sailors is less than min_occupancy.")
        sys.exit(1)

    if len(event_sailors) > max_overall:
        print("Number of sailors is greater than max_occupancy.")
        sys.exit(1)

    overall_occupancy = min_overall

    # Repeatedly add 1 to the occupancy of the boat with the greatest headroom,
    # until overall_occupancy is equal to the number of sailors.

    while len(event_sailors) > overall_occupancy:
        event_boats = order_boats_by_headroom(event_boats)
        for boat in database.boats_data:
            if event_boats[-1] == boat["key"]:
                boat["actual_occupancy"] = str(int(boat["actual_occupancy"]) + 1)
                overall_occupancy += 1

    extended_flotilla = {}
    extended_flotilla["flotilla"] = assign(event_boats, event_sailors)
    extended_flotilla["wait list"] = []

    return extended_flotilla

def assign(event_boats, event_sailors):

    # Return crews, which is a list of crew by assigning sailors to boats.

    # Reorder boats by boat loyalty,
    # Randomize the sailors list before.
    # Then assign boats and sailors to crews
    # until the number of sailors assigned to each boat is equal to its occupancy.
    # initial and final are the indices in sailors list of the first and last
    # sailors assigned to a boat.

    crews = []

    shuffled_sailors = []
    while len(event_sailors) > 0:
        sailor = event_sailors[random.randint(0, len(event_sailors) - 1)]
        event_sailors.remove(sailor)
        shuffled_sailors.append(sailor)

    initial = 0

    boats = order_boats_by_loyalty(event_boats)

    for event_boat in event_boats:
        crew = {}
        crew["boat"] = event_boat
        final = initial + [int(boat["actual_occupancy"]) for boat in database.boats_data if boat["key"] == event_boat][0]
        crew["sailors"] = shuffled_sailors[initial : final]
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

    for event_sailor in sailors:
        for sailor in database.sailors_data:
            if event_sailor == sailor["key"]:
                if sailor["member"] == "True":
                    members.append(event_sailor)
                else:
                    non_members.append(event_sailor)

    # Order members and non-members into lists of sailors in the same loyalty band.

    i = len(members)
    loyalty = 0
    while i > 0:
        equal_loyalty_members = [] # list of members in the same loyalty band.
        for member in members:
            for sailor in database.sailors_data:
                if member == sailor["key"]:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_members.append(member)
                        i -= 1
        loyalty += 1
        ordered_members.extend(equal_loyalty_members)

    i = len(non_members)
    loyalty = 0
    while i > 0:
        equal_loyalty_non_members = []
        for non_member in non_members:
            for sailor in database.sailors_data:
                if non_member == sailor["key"]:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_non_members.append(non_member)
                        i -= 1
        loyalty += 1
        ordered_non_members.extend(equal_loyalty_non_members)

    # For members first and then for non-members, randomize the order within each loyalty band.
    # Ordered_sailors will then contain the list of sailors in priority order.
    # First, members are prioritized over non-members.
    # Then those in low loyalty bands are prioritized over those in higher bands.

    loyalty = 0
    while len(ordered_members) > 0:
        equal_loyalty_members = []
        for member in ordered_members:
            for sailor in database.sailors_data:
                if member == sailor["key"]:
                    equal_loyalty_members.append(member)
        while len(equal_loyalty_members) > 0:
            if len(equal_loyalty_members) > 1:
                member_number = random.randint(0, len(equal_loyalty_members) - 1)
            else:
                member_number = 0
            next_member = equal_loyalty_members[member_number]
            equal_loyalty_members.remove(next_member)
            ordered_sailors.append(next_member)
            ordered_members.remove(next_member)
        loyalty += 1

    loyalty = 0
    while len(ordered_non_members) > 0:
        equal_loyalty_non_members = []
        for non_member in ordered_non_members:
            for sailor in database.sailors_data:
                if non_member == sailor["key"]:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_non_members.append(non_member)
        while len(equal_loyalty_non_members) > 0:
            if len(equal_loyalty_non_members) > 1:
                non_member_number = random.randint(0, len(equal_loyalty_non_members) - 1)
            else:
                non_member_number = 0
            next_non_member = equal_loyalty_non_members[non_member_number]
            equal_loyalty_non_members.remove(next_non_member)
            ordered_sailors.append(next_non_member)
            ordered_non_members.remove(next_non_member)
        loyalty += 1

    return ordered_sailors


def order_boats_by_loyalty(boats):

    # Create a list that orders boats by their loyalty band.
    # The order of boats in the same loyalty band is randomized.

    ordered_boats = []
    banded_boats = [] # A list of lists of boats in the same loyalty band.

    i = len(boats)
    loyalty = 0
    while i > 0:
        equal_loyalty_boats = [] # list of boats in the same loyalty band.
        for event_boat in boats:
            for boat in database.boats_data:
                if event_boat == boat["key"]:
                    if int(boat["loyalty"]) == loyalty:
                        equal_loyalty_boats.append(event_boat)
                        i -= 1
        loyalty += 1
        banded_boats.append(equal_loyalty_boats)

    while len(banded_boats) > 0:
        while len(banded_boats[0]) > 0:
            if len(banded_boats[0]) > 1:
                boat_number = random.randint(0, len(banded_boats[0]) - 1)
            else:
                boat_number = 0
            ordered_boats.append(banded_boats[0][boat_number])
            banded_boats[0].pop(boat_number)
        banded_boats.pop(0)

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
        for event_boat in boats:
            for boat in database.boats_data:
                if event_boat == boat["key"]:
                    if int(boat["max occupancy"]) - int(boat["actual_occupancy"]) == headroom:
                        headroom_boats.append(event_boat)
                        i -= 1
        headroom += 1
        banded_boats.append(headroom_boats)

    while len(banded_boats) > 0:
        while len(banded_boats[0]) > 0:
            if len(banded_boats[0]) > 1:
                boat_number = random.randint(0, len(banded_boats[0]) - 1)
            else:
                boat_number = 0
            ordered_boats.append(banded_boats[0][boat_number])
            banded_boats[0].pop(boat_number)
        banded_boats.pop(0)

    return ordered_boats
