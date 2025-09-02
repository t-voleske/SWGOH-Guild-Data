import os

def check_none(possible_none_value, error_str : str):
    if possible_none_value == None:
        raise ValueError(error_str)
    return possible_none_value

def is_list_or_tuple_instance(l):
    if isinstance(l, (list, tuple)):
        return l
    else:
        raise ValueError('read_players is not returning a list or tuple. Check read_players function')