import constants
import database
import math
import copy
import random


def max_berths(boat_keys, event_id):

    # Return the maximum number of berths available.

    berths = 0
    for boat_key in boat_keys:
        berths += int([boat[event_id] for boat in database.boats_availability if boat["key"] == boat_key][0])

    return berths

def min_berths(boat_keys):

    # Return the minimum number of sailors required.

    berths = 0
    for boat_key in boat_keys:
        berths += int([boat["min occupancy"] for boat in database.boats_data if boat["key"] == boat_key][0])

    return berths

def remove_flex_sailor_keys(boat_keys, sailor_keys):

    # Return the list of sailors who do not own one of the boats.

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

def boat_from_sailor(sailor_key):

    # Return the boat that is owned by the sailor.

    added_boat_key = [boat["key"] for boat in database.boats_data if boat["owner key"] == sailor_key][0]
    return added_boat_key


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


def shuffle(unshuffled_list):

    shuffled_list = []

    while len(unshuffled_list) > 0:
        if len(unshuffled_list) > 1:
            list_index = random.randint(0, len(unshuffled_list) - 1)
        else:
            list_index = 0
        next_entry = unshuffled_list[list_index]
        unshuffled_list.remove(next_entry)
        shuffled_list.append(next_entry)

    return shuffled_list


def prioritize_category_keys(category_list):

    # Separate the category list into loyalty bands, shuffle each band and return the category list
    # prioritized by loyalty and shuffled. Least loyalty has highest priority.

    prioritized_category_list = []
    progress = 0
    for loyalty in range( len( constants.event_ids )):
        if progress >= len( category_list ): break
        band = [sailor["key"] for sailor in database.sailors_data if category_list.count(sailor["key"]) > 0\
                and sailor["loyalty"] == str(loyalty)]
        if not len( band ) == 0:
            progress += len( band )
            prioritized_category_list.extend(band)

    return prioritized_category_list


def prioritize_sailor_keys(unprioritized_sailors):

    # Separate the sailor list into categories.  Prioritize each category by loyalty (least first).
    # Extend prioritized_sailors by each category in turn.  Return prioritized_sailors.

    prioritized_sailors = []

    category = [sailor["key"] for sailor in database.sailors_data if unprioritized_sailors.count(sailor["key"]) > 0\
            and sailor["category"] == 'G'\
            and sailor["member"].upper() == "TRUE"]
    prioritized_sailors.extend(prioritize_category_keys(category))

    category = [sailor["key"] for sailor in database.sailors_data if unprioritized_sailors.count(sailor["key"]) > 0\
            and sailor["category"] == 'G'\
            and sailor["member"].upper() == "FALSE"]
    prioritized_sailors.extend(prioritize_category_keys(category))

    category = [sailor["key"] for sailor in database.sailors_data if unprioritized_sailors.count(sailor["key"]) > 0\
            and sailor["category"] == 'A'\
            and sailor["member"].upper() == "TRUE"]
    prioritized_sailors.extend(prioritize_category_keys(category))

    category = [sailor["key"] for sailor in database.sailors_data if unprioritized_sailors.count(sailor["key"]) > 0\
            and sailor["category"] == 'A'\
            and sailor["member"].upper() == "FALSE"]
    prioritized_sailors.extend(prioritize_category_keys(category))

    category = [sailor["key"] for sailor in database.sailors_data if unprioritized_sailors.count(sailor["key"]) > 0\
            and sailor["category"] == 'N']
    prioritized_sailors.extend(prioritize_category_keys(category))

    return prioritized_sailors


def assign(boat_keys, sailor_keys, event_id):

    # Create crews by adding boat_keys to an initially-empty list of crews.

    crew = {}
    crews = []

    for boat_key in boat_keys:
        crew["boat"] = boat_key
        crews.append(copy.copy(crew))

    # Calculate sailors_per_space.  Once boat minimums have been satisfied, additionsl sailors should be distributed
    # between boats according to their remaining capacity.

    space_min = 0
    space_max = 0
    for boat_key in boat_keys:
        space_min += [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == boat_key][0]
        space_max += int([boat[event_id] for boat in database.boats_availability if boat["key"] == boat_key][0])
        # space_max += [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == boat_key][0]

    space_spread = space_max - space_min
    sailors_max = len(sailor_keys)
    sailors_spread = sailors_max - space_min

    if space_spread == 0:
        sailors_per_space = 0.0
    else:
        sailors_per_space = float(sailors_spread) / float(space_spread)

    # sailor_keys lists sailors in priority order.  So, assign sailors from the list in order.

    final_flt = 0.0
    initial_int = 0
    for i in range(len(crews) - 1):
        min = [int(boat["min occupancy"]) for boat in database.boats_data if boat["key"] == crews[i]["boat"]][0]
        max = int([boat[event_id] for boat in database.boats_availability if boat["key"] == crews[i]["boat"]][0])
        # max = [int(boat["max occupancy"]) for boat in database.boats_data if boat["key"] == crews[i]["boat"]][0]
        spread = max - min
        final_flt += float(min) + float(spread) * sailors_per_space
        final_int = math.ceil(final_flt)
        crews[i]["sailors"] = sailor_keys[initial_int : final_int]
        initial_int = final_int
    if len(crews) > 0:
        crews[-1]["sailors"] = sailor_keys[initial_int : ]

    return crews


def mandatory(all_boat_keys, all_sailor_keys, event_id):

    # flex sailors are sailors who own a boat and who have made their boat available.
    # flex boats are boats whose owners have made themselves available to crew.

    core_sailor_keys = remove_flex_sailor_keys(all_boat_keys, all_sailor_keys)
    core_boat_keys = remove_flex_boat_keys(all_boat_keys, all_sailor_keys)
    wait_sailor_keys = []
    wait_boat_keys = []

    # Separate the cases of over-demand, over-supply and matching supply and demand.

    if len(core_sailor_keys) > max_berths(all_boat_keys, event_id): # over-demand - cut sailors
        while len(core_sailor_keys) > max_berths(all_boat_keys, event_id):
            redundant_sailor_key = prioritize_sailor_keys(core_sailor_keys)[-1]
            core_sailor_keys.remove(redundant_sailor_key)
            wait_sailor_keys.insert(0, redundant_sailor_key)

        event_boat_keys = copy.deepcopy(all_boat_keys)
        event_sailor_keys = copy.deepcopy(shuffle(core_sailor_keys))

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

        while len(sailor_keys) > max_berths(boat_keys, event_id):
            flex_sailor_keys = [sailor_key for sailor_key in sailor_keys if sailor_key not in core_sailor_keys]
            skipper_key = order_sailor_keys(flex_sailor_keys)[-1]
            sailor_keys.remove(skipper_key)
            boat_keys.append(boat_from_sailor(skipper_key))

        event_boat_keys = copy.deepcopy(boat_keys)
        event_sailor_keys = copy.deepcopy(sailor_keys)

    event = {}
    event["flotilla"] = assign(event_boat_keys, event_sailor_keys, event_id)
    event["wait list"] = wait_sailor_keys

    return event
