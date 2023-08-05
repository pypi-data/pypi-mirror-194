import re

from ..base import BaseListener
from ..utils import (
    QueryParameter,
    TopicListenerStatusObject,
    TopicListenerOperation,
    ExtrinsicCall,
)

METARIUM_EXTRINSIC = "Metarium"

OPERATION = TopicListenerOperation()


class TopicListenerStatusListener(BaseListener):

    def __processed_block(self, block):
        processed_block = {
            "block_number": block["header"]["number"],
            "extrinsics": []
        }
        for extrinsic in block["extrinsics"]:
            extrinsic = extrinsic.serialize()
            # print(f"{extrinsic = }")
            if extrinsic["call"]["call_module"] == METARIUM_EXTRINSIC:
                call = ExtrinsicCall(
                    call_function=extrinsic["call"]["call_function"],
                    call_index=extrinsic["call"]["call_index"],
                    caller=extrinsic["address"]
                )
                status_value, rff_value = None, None
                if call.call_function == OPERATION.self_update:
                    status_value = extrinsic["call"]["call_args"][0]["value"]
                    rff_value = extrinsic["call"]["call_args"][1]["value"]

                # TODO:
                # OPERATION.add, OPERATION.delete, OPERATION.sudo_update

                if status_value is not None and rff_value is not None:
                    processed_block["extrinsics"].append(
                        TopicListenerStatusObject(
                            status=status_value,
                            rff=rff_value,
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
                for service_status_object in extrinsics:
                    assert isinstance(service_status_object,
                                      TopicListenerStatusObject)
                    extrinsic = service_status_object._asdict()
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
