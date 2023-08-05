from collections import namedtuple


METARIUM_FUNCTION_CALL_SCRIBE_STATUS_UPDATE_BY_ADMIN = "force_update_scribe_authority_status"
METARIUM_FUNCTION_CALL_SCRIBE_STATUS_UPDATE_BY_SCRIBE = "update_scribe_authority_status"

ScribeObject = namedtuple(
    "ScribeObject",
    "scribe call_function caller call_index",
    defaults=[None, None, None, None]
)

ScribeOperation = namedtuple(
    "ScribeOperation",
    "admin_updated_scribe scribe_updated_scribe",
    defaults=[
        METARIUM_FUNCTION_CALL_SCRIBE_STATUS_UPDATE_BY_ADMIN,
        METARIUM_FUNCTION_CALL_SCRIBE_STATUS_UPDATE_BY_SCRIBE
    ]
)