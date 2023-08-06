"""
Constants for the braze client.
"""


class BrazeAPIEndpoints:
    """
    Braze endpoints.
    """

    SEND_CAMPAIGN = '/campaigns/trigger/send'
    SEND_CANVAS = '/canvas/trigger/send'
    EXPORT_IDS = '/users/export/ids'
    SEND_MESSAGE = '/messages/send'
    NEW_ALIAS = '/users/alias/new'
    TRACK_USER = '/users/track'
    IDENTIFY_USERS = '/users/identify'
    UNSUBSCRIBE_USER_EMAIL = '/email/status'


# Braze enforced request size limits
TRACK_USER_COMPONENT_CHUNK_SIZE = 75
USER_ALIAS_CHUNK_SIZE = 50
UNSUBSCRIBED_STATE = 'unsubscribed'
