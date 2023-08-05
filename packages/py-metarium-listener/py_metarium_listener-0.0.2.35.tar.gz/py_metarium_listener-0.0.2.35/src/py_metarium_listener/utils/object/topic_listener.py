from collections import namedtuple

METARIUM_FUNCTION_CALL_TOPIC_LISTENER_ADD = "node_added_to_topic_listener_set"
METARIUM_FUNCTION_CALL_TOPIC_LISTENER_DELETE = "node_deleted_from_topic_listener_set"
METARIUM_FUNCTION_CALL_TOPIC_LISTENER_SELF_UPDATE = "topic_listener_node_status_updated"
METARIUM_FUNCTION_CALL_TOPIC_LISTENER_SUDO_UPDATE = "force_update_topic_listener_node"

TopicListenerStatusObject = namedtuple(
    "TopicListenerStatusObject",
    "topic_id status rff call_function caller call_index",
    defaults=[None, None, None, None, None, None]
)

TopicListenerOperation = namedtuple(
    "TopicListenerOperation",
    "add delete self_update sudo_update",
    defaults=[
        METARIUM_FUNCTION_CALL_TOPIC_LISTENER_ADD,
        METARIUM_FUNCTION_CALL_TOPIC_LISTENER_DELETE,
        METARIUM_FUNCTION_CALL_TOPIC_LISTENER_SELF_UPDATE,
        METARIUM_FUNCTION_CALL_TOPIC_LISTENER_SUDO_UPDATE,
    ]
)
