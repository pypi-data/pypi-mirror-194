import string
import random
import json
from hashlib import md5
from typing import Optional


def dict_to_json_file(d_dict, file_name):
    """write a dict (d_dict) as json to a file (file_name)."""
    with open(file_name, "w+") as out_file:
        json.dump(d_dict, out_file)


def randstring(k_=32, alphabet: Optional[str] = None):
    """well behaving random string (chars chosen from a curated "alphabet")
    :param k_: length of the string to be generated
    :param alphabet: override default alphabet by providing a string here
    :returns: string sans stuff what might mess up a python str or upset pylint
    """
    if not alphabet:
        alphabet = "!&*+-=?@_~"
        # removed $%^ - in particular '%' did not behave well with logger methods
        alphabet += string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=k_))


def split_name(a_name):
    """
    If only one word given, return it as last.
    If more than two words given, return all but last as first.
    examples = {
        'ok simple': ('ok', 'simple'),
        'solo': ('', 'solo'),
        'three part name': ('three part', 'name'),
        'name with-hyphen': ('name', 'with-hyphen'),
        '': ('', '')
        }
    :param a_name: str
    :return: ('first', 'last')
    """
    try:
        a_split = a_name.split()
        last = a_split[-1]
        first = " ".join(a_split[:-1])
        if not len(first) or not last:
            # no_first_name_count += 1
            first = ""
        return first, last
    except IndexError:
        return "", ""


# end def split_name()


def obsc_email(email_address):
    """
    obscure and email address:
    'something@example.com' -> 'som...@e...'
    """
    ls = email_address.strip().split("@")
    return ls[0][0:3] + "...@" + ls[1][0] + "..."


def path_is_url(path: str) -> bool:
    """returns True when input starts either http:// Or https://"""  # noqa
    return any(
        (
            path[:7] == "http://",  # noqa suppress 'HTTP not secure' warning
            path[:8] == "https://",
        )
    )


def str_hash(input_str: str) -> str:
    """
    Get the md5 hash for a normalised string,
    based on Gravatar hash implementation.
    Designed for email addresses; can hash any string.

    ref: https://en.gravatar.com/site/implement/hash/
        To ensure a consistent and accurate hash,
        the following steps should be taken to create a hash:
            1. Trim leading and trailing whitespace from an email address
            2. Force all characters to lower-case
            3. md5 hash the final string
    :param input_str: can be any string
    :return: md5 hash of the normalised string
    """
    return md5(input_str.strip().lower().encode()).hexdigest()
