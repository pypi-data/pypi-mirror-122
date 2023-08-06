# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.
#
# based on tweepy(https://github.com/tweepy/tweepy)
# Copyright (c) 2009-2021 Joshua Roesslein

from .parser import Parser

class RawParser(Parser):
    def __init__(self):
        pass

    @classmethod
    def parse(cls, payload, *args, **kwargs):
        return payload
