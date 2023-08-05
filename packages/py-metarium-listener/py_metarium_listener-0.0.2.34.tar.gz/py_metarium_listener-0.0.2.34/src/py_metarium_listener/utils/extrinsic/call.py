from collections import namedtuple

ExtrinsicCall = namedtuple(
    "ExtrinsicCall",
    "call_function call_index caller"
)