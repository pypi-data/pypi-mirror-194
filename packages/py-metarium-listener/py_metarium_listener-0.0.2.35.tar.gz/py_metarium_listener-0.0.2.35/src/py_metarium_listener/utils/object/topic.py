from collections import namedtuple

METARIUM_FUNCTION_CALL_TOPIC_CREATE = "topic_added"
METARIUM_FUNCTION_CALL_TOPIC_ADD_COMMITTER = "node_added_to_topic_committer_set"
METARIUM_FUNCTION_CALL_TOPIC_REMOVE_COMMITTER = "node_removed_from_topic_committer_set"
METARIUM_FUNCTION_CALL_TOPIC_ADD_LISTENER = "node_added_to_topic_listener_set"
METARIUM_FUNCTION_CALL_TOPIC_REMOVE_LISTENER = "node_removed_from_topic_listener_set"
METARIUM_FUNCTION_CALL_TOPIC_TOGGLE_PAUSE = "topic_pause_toggled"
METARIUM_FUNCTION_CALL_TOPIC_ARCHIVE = "topic_archived"
METARIUM_FUNCTION_CALL_TOPIC_UNARCHIVE = "force_unarchive_topic"
METARIUM_FUNCTION_CALL_TOPIC_TOGGLE_TRANSFER_ACCEPTANCE = "topic_transfer_acceptance_toggled"
METARIUM_FUNCTION_CALL_TOPIC_TRANSFER = "topic_transferred"
METARIUM_FUNCTION_CALL_TOPIC_UPDATE_CONFIGURER = "topic_configuration_node_changed"

TopicObject = namedtuple(
    "TopicObject",
    "topic call_function caller call_index",
    defaults=[None, None, None, None]
)

TopicOperation = namedtuple(
    "TopicOperation",
    "create add_committer remove_committer add_listener remove_listener toggle_pause archive unarchive toggle_transfer_acceptance transfer update_configurer",
    defaults=[
        METARIUM_FUNCTION_CALL_TOPIC_CREATE,
        METARIUM_FUNCTION_CALL_TOPIC_ADD_COMMITTER,
        METARIUM_FUNCTION_CALL_TOPIC_REMOVE_COMMITTER,
        METARIUM_FUNCTION_CALL_TOPIC_ADD_LISTENER,
        METARIUM_FUNCTION_CALL_TOPIC_REMOVE_LISTENER,
        METARIUM_FUNCTION_CALL_TOPIC_TOGGLE_PAUSE,
        METARIUM_FUNCTION_CALL_TOPIC_ARCHIVE,
        METARIUM_FUNCTION_CALL_TOPIC_UNARCHIVE,
        METARIUM_FUNCTION_CALL_TOPIC_TOGGLE_TRANSFER_ACCEPTANCE,
        METARIUM_FUNCTION_CALL_TOPIC_TRANSFER,
        METARIUM_FUNCTION_CALL_TOPIC_UPDATE_CONFIGURER
    ]
)
