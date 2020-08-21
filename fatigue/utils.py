import json


def load_json(jsonfile, ordered=False):
    """
    Load data/varibles from .json-file

    :param jsonfile: str
            .json file (name or full path) to load
    :param ordered: bool
            If false a standard (unordered) dictonary is used. If true, a collections.OrderedDict
        instance is returned and the order of the jsonfile is preserved.

    :return:
    """

    if ordered is True:
        d = OrderedDict
    else:
        d = None

    with open(jsonfile, 'r') as fp:
        data = json.load(fp, object_pairs_hook=d)

    return data


def is_number(s):
    """Check if data is number"""
    try:
        float(s)
        return True
    except ValueError:
        return False


def from_dict(cls, d):
    """Create class from dictionary"""
    c = cls()
    c.r = d.get("r")
    c.z = d.get("z")
    c.max_element_length = d.get("max_element_length")
    return c
