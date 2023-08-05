from py_metarium import (PAST, FUTURE)

from py_metarium_listener import (
    BlockListener,
    AriKuriListener,
    TopicListenerStatusListener,
    QueryParameter
)

# CONSTANTS
ARCHIVE_NODE_URL = "wss://node-7006463752615444480.gx.onfinality.io/ws?apikey=59626ed4-2dca-40b5-9e3b-d3c481769f17"
VALIDATOR_NODE_URL = "wss://node-7002861606479888384.gx.onfinality.io/ws?apikey=26c3cb95-b28b-4de3-8cf7-010553c76b12"
LOCALHOST_NODE_URL = "ws://127.0.0.1:9945"

# set metarium_node_url
metarium_node_url = LOCALHOST_NODE_URL

# # set query
# query = [
#     QueryParameter("caller", "^5DRPjWc35HTPhniGhE8DoBSKs3hinpkjQ9Bf1hkciQdJkUZq$"),
#     # QueryParameter("kuri", "^love$"),
#     QueryParameter("kuri", "^\|\>ipfs\|.*")
# ]

# # set folder
# folder = "listened"

# # set filename
# filename = "all"
# if len(query):
#     filename = ""
#     for param in query:
#         if len(filename):
#             filename += "&"
#         filename += f"{param.field}={param.value}"
# filename += ".py"

# # listen
# kuri_listener = KuriListener(metarium_node_url)
# print("listening ...")

# file_location = f"{folder}/{filename}"
# with open(f"{file_location}", "w") as f:
#     for block in kuri_listener.listen(
#                 FUTURE,
#                 "0x1165b345b939550135a2a67a6ef70ca3495437a53513d887a969a51cbac7697f",
#                 None,
#                 query=query
#             ):
#         # print(f"{block['header']['number']}")
#         print(f"{block}\n")
#         f.write(f"\n{block}")


# t = BlockListener(metarium_node_url)
# for block in t.listen(
#             FUTURE,
#             "0x1165b345b939550135a2a67a6ef70ca3495437a53513d887a969a51cbac7697f",
#             None
#         ):
#     # print(f"{block['header']['number']}")
#     print(f"{block}\n")


# t = ServiceStatusListener(metarium_node_url)
topic_id = 441
t = AriKuriListener(metarium_node_url)
for block in t.listen(
    FUTURE,
    None,
    None,
    query=[
        QueryParameter("topic_id", f"^{topic_id}$"),
        # QueryParameter("kuri", "^love$"),
        # QueryParameter("kuri", "^\|\>ipfs\|.*")
    ]
):
    # print(f"{block['header']['number']}")
    print(f"{block = }\n")
