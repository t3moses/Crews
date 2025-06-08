
import database
import math
import copy
import random


def max_berths(boat_keys):

# Return the maximum number of berths available.

    berths = 0
    for boat_key in boat_keys:
        berths += int([boat["max occupancy"] for boat in database.boats_data if boat["key"] == boat_key][0])

    return berths

def min_berths(boat_keys):

# Return the minimum number of sailors required.

    berths = 0
    for boat_key in boat_keys:
        berths += int([boat["min occupancy"] for boat in database.boats_data if boat["key"] == boat_key][0])

    return berths

def remove_flex_sailor_keys(boat_keys, sailor_keys):

# Return the list of sailors that do not own one of the boats.

    core_sailor_keys = copy.deepcopy(sailor_keys)
    for sailor_key in sailor_keys:
        for boat_key in boat_keys:
            for boat in database.boats_data:        
                if boat_key == boat["key"] and sailor_key == boat["owner key"]:
                    core_sailor_keys.remove(sailor_key)
    return core_sailor_keys

def remove_flex_boat_keys(boat_keys, sailor_keys):

# Return the list of boats whose owners are not amongst the sailors.

    core_boat_keys = copy.deepcopy(boat_keys)
    for sailor_key in sailor_keys:
        for boat_key in boat_keys:
            for boat in database.boats_data:
                if boat_key == boat["key"] and sailor_key == boat["owner key"]:
                    core_boat_keys.remove(boat_key)
    return core_boat_keys

def remove_most_loyal_sailor_key(sailor_keys):

# Return the list of sailors having removed the one who has sailed most.

    ordered_sailor_keys = order_sailor_keys(sailor_keys)
    ordered_sailor_keys.pop(-1)
    return ordered_sailor_keys

def remove_most_loyal_boat_key(boat_keys):

    # Return the list of boats having removed the one who has sailed most.

    ordered_boat_keys = order_boat_keys_by_loyalty(boat_keys)
    ordered_boat_keys.pop(-1)
    return ordered_boat_keys

def boat_from_sailor(sailor_key):

# Return the boat that is owned by the sailor.

    added_boat_key = [boat["key"] for boat in database.boats_data if boat["owner key"] == sailor_key][0]
    return added_boat_key

def mandatory(all_boat_keys, all_sailor_keys):

    core_sailor_keys = remove_flex_sailor_keys(all_boat_keys, all_sailor_keys)
    core_boat_keys = remove_flex_boat_keys(all_boat_keys, all_sailor_keys)
    wait_sailor_keys = []
    wait_boat_keys = []

    if len(core_sailor_keys) > max_berths(all_boat_keys): # over-demand - cut sailors
        while len(core_sailor_keys) > max_berths(all_boat_keys):
            redundant_sailor_key = order_sailor_keys(core_sailor_keys)[-1]
            core_sailor_keys.remove(redundant_sailor_key)
            wait_sailor_keys.insert(0, redundant_sailor_key)

        event_boat_keys = copy.deepcopy(all_boat_keys)
        event_sailor_keys = copy.deepcopy(core_sailor_keys)

    elif len(all_sailor_keys) < min_berths(core_boat_keys): # over-supply - cut boats:
        while len(all_sailor_keys) < min_berths(core_boat_keys) and len(core_boat_keys) > 1:
            redundant_boat_key = order_boat_keys_by_loyalty(core_boat_keys)[-1]
            core_boat_keys.remove(redundant_boat_key)
            wait_boat_keys.append(redundant_boat_key)

        event_boat_keys = copy.deepcopy(core_boat_keys)
        event_sailor_keys = copy.deepcopy(all_sailor_keys)

    else: # supply and demand can match

        sailor_keys = copy.copy(all_sailor_keys)
        boat_keys = copy.copy(core_boat_keys)

        while len(sailor_keys) > max_berths(boat_keys):
            flex_sailor_keys = [sailor_key for sailor_key in sailor_keys if sailor_key not in core_sailor_keys]
            skipper_key = order_sailor_keys(flex_sailor_keys)[-1]
            sailor_keys.remove(skipper_key)
            boat_keys.append(boat_from_sailor(skipper_key))

        event_boat_keys = copy.deepcopy(boat_keys)
        event_sailor_keys = copy.deepcopy(sailor_keys)

    event = {}
    event["flotilla"] = assign(event_boat_keys, event_sailor_keys)
    event["wait list"] = wait_sailor_keys

    return event


def assign(boat_keys, sailor_keys):

    # Create shuffled_sailor_keys by randomly shuffling sailor_keys.

    shuffled_sailor_keys = []
    while len(sailor_keys) > 0:
        sailor_key = sailor_keys[random.randint(0, len(sailor_keys) - 1)]
        sailor_keys.remove(sailor_key)
        shuffled_sailor_keys.append(sailor_key)

    # Create crews by adding boat_keys to an initially-empty list of crews.

    crew = {}
    crews = []

    for boat_key in boat_keys:
        crew["boat"] = boat_key
        crews.append(copy.copy(crew))

    # Calculate sailors_per_space.

    space_min = 0
    space_max = 0
    for boat_key in boat_keys:
        space_min += [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == boat_key][0]
        space_max += [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == boat_key][0]

    space_spread = space_max - space_min
    sailors_max = len(shuffled_sailor_keys)
    sailors_spread = sailors_max - space_min

    if space_spread == 0:
        sailors_per_space = 0.0
    else:
        sailors_per_space = float(sailors_spread) / float(space_spread)

    final_flt = 0.0
    initial_int = 0
    for i in range(len(crews) - 1):
        min = [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == crews[i]["boat"]][0]
        max = [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == crews[i]["boat"]][0]
        spread = max - min
        final_flt += float(min) + float(spread) * sailors_per_space
        final_int = math.ceil(final_flt)
        crews[i]["sailors"] = shuffled_sailor_keys[initial_int : final_int]
        initial_int = final_int
    if len(crews) > 0:
        crews[-1]["sailors"] = shuffled_sailor_keys[initial_int : ]

    return crews


def order_sailor_keys(sailor_keys):

    # Create a list that orders sailor keys by their membership status and loyalty band.
    # The order of sailors in the same loyalty band is randomized.

    member_keys = []
    non_member_keys = []
    ordered_member_keys = []
    ordered_non_member_keys = []
    ordered_sailor_keys = []

    # Divide sailors into members and non-members.

    for sailor_key in sailor_keys:
        for sailor in database.sailors_data:
            if sailor["key"] == sailor_key:
                if sailor["member"].upper() == "TRUE":
                    member_keys.append(sailor_key)
                else:
                    non_member_keys.append(sailor_key)

    # Order members and non-members into lists of sailors in the same loyalty band.

    i = len(member_keys)
    loyalty = 0
    while i > 0:
        equal_loyalty_member_keys = [] # list of members in the same loyalty band.
        for member_key in member_keys:
            for sailor in database.sailors_data:
                if sailor["key"] == member_key:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_member_keys.append(member_key)
                        i -= 1
        loyalty += 1
        ordered_member_keys.extend(equal_loyalty_member_keys)

    i = len(non_member_keys)
    loyalty = 0
    while i > 0:
        equal_loyalty_non_member_keys = []
        for non_member_key in non_member_keys:
            for sailor in database.sailors_data:
                if sailor["key"] == non_member_key:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_non_member_keys.append(non_member_key)
                        i -= 1
        loyalty += 1
        ordered_non_member_keys.extend(equal_loyalty_non_member_keys)

    # For members first and then for non-members, randomize the order within each loyalty band.
    # Ordered_sailors will then contain the list of sailors in priority order.
    # First, members are prioritized over non-members.
    # Then those in low loyalty bands are prioritized over those in higher bands.

    loyalty = 0
    while len(ordered_member_keys) > 0:
        equal_loyalty_member_keys = []
        for member_key in ordered_member_keys:
            for sailor in database.sailors_data:
                if member_key == sailor["key"]:
                    equal_loyalty_member_keys.append(member_key)
        while len(equal_loyalty_member_keys) > 0:
            if len(equal_loyalty_member_keys) > 1:
                member_number = random.randint(0, len(equal_loyalty_member_keys) - 1)
            else:
                member_number = 0
            next_member = equal_loyalty_member_keys[member_number]
            equal_loyalty_member_keys.remove(next_member)
            ordered_sailor_keys.append(next_member)
            ordered_member_keys.remove(next_member)
        loyalty += 1

    loyalty = 0
    while len(ordered_non_member_keys) > 0:
        equal_loyalty_non_member_keys = []
        for non_member_key in ordered_non_member_keys:
            for sailor in database.sailors_data:
                if sailor["key"] == non_member_key:
                    if int(sailor["loyalty"]) == loyalty:
                        equal_loyalty_non_member_keys.append(non_member_key)
        while len(equal_loyalty_non_member_keys) > 0:
            if len(equal_loyalty_non_member_keys) > 1:
                non_member_number = random.randint(0, len(equal_loyalty_non_member_keys) - 1)
            else:
                non_member_number = 0
            next_non_member = equal_loyalty_non_member_keys[non_member_number]
            equal_loyalty_non_member_keys.remove(next_non_member)
            ordered_sailor_keys.append(next_non_member)
            ordered_non_member_keys.remove(next_non_member)
        loyalty += 1

    return ordered_sailor_keys


def order_boat_keys_by_loyalty(boat_keys):

    # Create a list that orders boats by their loyalty band.
    # The order of boats in the same loyalty band is randomized.

    ordered_boat_keys = []
    banded_boat_keys = [] # A list of lists of boats in the same loyalty band.

    i = len(boat_keys)
    loyalty = 0
    while i > 0:
        equal_loyalty_boat_keys = [] # list of boats in the same loyalty band.
        for event_boat_key in boat_keys:
            for boat in database.boats_data:
                if event_boat_key == boat["key"]:
                    if int(boat["loyalty"]) == loyalty:
                        equal_loyalty_boat_keys.append(event_boat_key)
                        i -= 1
        loyalty += 1
        banded_boat_keys.append(equal_loyalty_boat_keys)

    while len(banded_boat_keys) > 0:
        while len(banded_boat_keys[0]) > 0:
            if len(banded_boat_keys[0]) > 1:
                boat_number = random.randint(0, len(banded_boat_keys[0]) - 1)
            else:
                boat_number = 0
            ordered_boat_keys.append(banded_boat_keys[0][boat_number])
            banded_boat_keys[0].pop(boat_number)
        banded_boat_keys.pop(0)

    return ordered_boat_keys
