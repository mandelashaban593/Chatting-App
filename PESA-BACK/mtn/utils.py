'''
mtn app utils
'''
import string
import random


def random_string_generator(string_len):
    """
    generate random string with length "string_len"
    """

    random_string = ''.join(random.choice(
        string.ascii_uppercase) for i in range(string_len))
    return random_string
