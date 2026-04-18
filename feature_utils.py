import numpy as np
import math

def username_entropy(username):
    prob = [username.count(c) / len(username) for c in set(username)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy


def digit_ratio(username):
    digits = sum(c.isdigit() for c in username)
    return digits / len(username)


def underscore_count(username):
    return username.count("_")


def username_length(username):
    return len(username)