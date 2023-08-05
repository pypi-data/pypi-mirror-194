from collections import namedtuple

METARIUM_FUNCTION_CALL_ARIKURI_ADD = "arikuri_added"
METARIUM_FUNCTION_CALL_ARIKURI_ACCEPT_MULTIPLE = "arikuri_transfers_accepted"
METARIUM_FUNCTION_CALL_ARIKURI_TRANSFER_MULTIPLE = "arikuris_transferred"
METARIUM_FUNCTION_CALL_ARIKURI_DELETE = "arikuri_deleted"
METARIUM_FUNCTION_CALL_ARIKURI_SUDO_UPDATE = "force_update_arikuri"

ArikuriObject = namedtuple(
    "ArikuriObject",
    "source_topic_id kuri destination_topic_id call_function caller call_index",
    defaults=[None, None, None, None, None, None]
)

ArikuriOperation = namedtuple(
    "ArikuriOperation",
    "add delete accept_multiple transfer_multiple sudo_update",
    defaults=[
        METARIUM_FUNCTION_CALL_ARIKURI_ADD,
        METARIUM_FUNCTION_CALL_ARIKURI_DELETE,
        METARIUM_FUNCTION_CALL_ARIKURI_ACCEPT_MULTIPLE,
        METARIUM_FUNCTION_CALL_ARIKURI_TRANSFER_MULTIPLE,
        METARIUM_FUNCTION_CALL_ARIKURI_SUDO_UPDATE,
    ]
)
