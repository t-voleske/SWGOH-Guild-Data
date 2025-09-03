

def check_none(possible_none_value, error_str : str):
    if possible_none_value is None:
        raise ValueError(error_str)
    return possible_none_value

def is_list_or_tuple_instance(check_value):
    if isinstance(check_value, (list, tuple)):
        return check_value
    else:
        raise ValueError('read_players is not returning a list or tuple. Check read_players function')