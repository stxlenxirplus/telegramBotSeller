import random
import string


def serialize(string: str):
    s = ''.join(string.split("&")[1::]).split('?')
    json_ = {}
    for param in s:
        key, value = param.split("=")
        json_[key] = value
    return json_


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def generate_id(len: int):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, len))

def generate_id_digits(len: int):
    digits = string.digits
    return random.randint(0, int('9'*len))
