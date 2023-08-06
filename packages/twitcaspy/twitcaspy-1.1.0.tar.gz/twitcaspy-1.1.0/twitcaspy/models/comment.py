# Twitcaspy
# Copyright 2021 Alma-field
# See LICENSE for details.

from ..utils import fromtimestamp

from .model import Model

from .user import User

class Comment(Model):
    """Comment Object

    Attributes
    ----------
    id: :class:`str`
        | |comment_id|
    message: :class:`str`
        | comment text
    from_user: :class:`~twitcaspy.models.User`
        | Comment contributor information
    created: :class:`datetime.datetime`
        | Converted created_time to :class:`datetime.datetime` type
    created_time: :class:`int`
        | Unix time stamp of comment posting datetime

    References
    ----------
    https://apiv2-doc.twitcasting.tv/#comment-object
    """

    @classmethod
    def parse(cls, api, json):
        comment = cls(api)
        setattr(comment, '_json', json)
        for k, v in json.items():
            if k == 'created':
                setattr(comment, k, fromtimestamp(v))
                setattr(comment, f'{k}_time', v)
            elif k == 'from_user':
                setattr(comment, k, User.parse(api, v))
            else:
                setattr(comment, k, v)
        return comment
