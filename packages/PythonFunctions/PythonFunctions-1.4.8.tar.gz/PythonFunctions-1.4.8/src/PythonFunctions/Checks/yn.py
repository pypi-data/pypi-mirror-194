"""
Returns True ("y") or False ("n")

Arguments:
----------
None
"""


def check(value, Message, _, **info):
    """
    If value == `y` then return True
    if value == `n` then return False
    else return None
    """
    value = value.strip()

    if len(value) == 0:
        return Message.clear("Invalid input! Nothing there")

    if info.get("y") and value[0].lower() == "y":
        return info.get("y")() or True
    if info.get("n") and value[0].lower() == "n":
        return info.get("n")() or True

    return True if value[0] == "y" else False if value[0] == "n" else None
