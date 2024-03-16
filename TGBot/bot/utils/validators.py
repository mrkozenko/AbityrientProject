import re


async def check_correct_name(name):
    # check if name is correct
    pattern = re.compile(r'[^\w\s_]')
    if pattern.search(name) is not None:
        return False
    return True


async def is_valid_phone(text):
    # check if phone number is correct
    regex = r"^\+?[0-9]{1,3}\d{1,14}$"
    return re.match(regex, text) is not None


async def is_valid_email(text):
    # check if mail valid
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    return re.match(regex, text) is not None
