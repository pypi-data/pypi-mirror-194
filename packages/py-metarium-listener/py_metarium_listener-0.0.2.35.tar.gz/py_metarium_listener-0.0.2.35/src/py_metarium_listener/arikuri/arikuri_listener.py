import re

from ..base import BaseListener
from ..utils import (
    QueryParameter,
    ArikuriObject,
    ArikuriOperation,
    ExtrinsicCall,
)

METARIUM_EXTRINSIC = "Metarium"

OPERATION = ArikuriOperation()


class AriKuriListener(BaseListener):

    def __processed_block(self, block):
        processed_block = {
            "block_number": block["header"]["number"],
            "extrinsics": []
        }
        for extrinsic in block["extrinsics"]:
            extrinsic = extrinsic.serialize()
            if extrinsic["call"]["call_module"] == METARIUM_EXTRINSIC:
                call = ExtrinsicCall(
                    call_function=extrinsic["call"]["call_function"],
                    call_index=extrinsic["call"]["call_index"],
                    caller=extrinsic["address"]
                )
                kuri_value, topic_id, destination_topic_id = None, None, None
                if call.call_function in (
                    OPERATION.add,
                    OPERATION.delete,
                    OPERATION.sudo_update
                ):
                    kuri_value = extrinsic["call"]["call_args"][0]["value"]
                    topic_id = extrinsic["call"]["call_args"][1]["value"]
                elif call.call_function in (
                    OPERATION.accept_multiple,
                    OPERATION.transfer_multiple,
                ):
                    kuri_value = extrinsic["call"]["call_args"][0]["value"]
                    topic_id = extrinsic["call"]["call_args"][1]["value"]
                    destination_topic_id = extrinsic["call"]["call_args"][2]["value"]
                if kuri_value is not None:
                    processed_block["extrinsics"].append(
                        ArikuriObject(
                            topic_id=topic_id,
                            kuri=kuri_value,
                            destination_topic_id=destination_topic_id,
                            call_function=call.call_function,
                            call_index=call.call_index,
                            caller=call.caller
                        )
                    )
        return processed_block

    def __listen(self, direction, block_hash=None, block_count=None):
        for block, is_metarium in self.decoder().decode_metarium(direction, block_hash=block_hash, block_count=block_count):
            yield block, is_metarium

    def listen(self, direction: str, block_hash: str = None, block_count: int = None, query: list = []):
        assert all(isinstance(parameter, QueryParameter)
                   for parameter in query)

        # print(f"\n\nQUERY IS {query}\n\n")

        for block, is_metarium in self.__listen(direction, block_hash, block_count):
            if not is_metarium:
                continue
            block = self.__processed_block(block)
            if len(query):
                extrinsics = block.pop("extrinsics")
                block["extrinsics"] = []
                for kuri_object in extrinsics:
                    assert isinstance(kuri_object, ArikuriObject)
                    extrinsic = kuri_object._asdict()
                    query_matches = 0
                    for parameter in query:
                        if (
                            (f"{parameter.field}" in extrinsic) and
                            (re.search(f"{parameter.value}",
                                       f"{extrinsic[parameter.field]}"))
                        ):
                            query_matches += 1
                    if query_matches == len(query):
                        block["extrinsics"].append(extrinsic)
                if not len(block["extrinsics"]):
                    continue

            yield block
