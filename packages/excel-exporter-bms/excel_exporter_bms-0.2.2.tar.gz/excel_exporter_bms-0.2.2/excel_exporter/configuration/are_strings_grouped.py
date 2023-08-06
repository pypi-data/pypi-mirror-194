from typing import List


def are_strings_grouped(list_of_strings: List[str]) -> bool:
    # First find the number of expected changes
    n_unique_strings = len(set(list_of_strings))
    n_expected_changes = n_unique_strings - 1
    # Then find the real number of changes
    groups_changes = [
        1
        for former, latter in zip(list_of_strings[:-1], list_of_strings[1:])
        if former != latter
    ]
    n_real_changes = sum(groups_changes)
    # Finally compare them
    return n_real_changes == n_expected_changes


# Grouped:
# _list_of_strings = ['a', 'a', 'a', 'b', 'b', 'b', 'c']
# _list_of_strings = ['a', 'a', b']
# _list_of_strings = ['a', 'b', b']
# _list_of_strings = ['a', 'b', c']
# _list_of_strings = ['a', 'b']
# _list_of_strings = ['a', 'a']
# _list_of_strings = ['a']
#
# Not Grouped:
# _list_of_strings = ['a', 'a', 'a', 'b', 'b', 'b', 'a']
# _list_of_strings = ['a', 'b', 'a', 'b', 'b', 'b', 'c']
# _list_of_strings = ['a', 'b', 'a', 'c', 'b', 'c', 'd']
# _list_of_strings = ['a', 'b', 'a', 'b', 'a', 'b', 'a']
# _list_of_strings = ['a', 'b', a']
