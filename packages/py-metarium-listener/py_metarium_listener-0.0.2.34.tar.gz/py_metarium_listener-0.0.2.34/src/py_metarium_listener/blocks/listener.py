from ..base import BaseListener


class BlockListener(BaseListener):

    def __listen(self, direction, block_hash=None, block_count=None):
        for block in self.decoder().decode_metarium(direction, block_hash=block_hash, block_count=block_count):
            yield block
    
    def listen(self, direction:str, block_hash:str=None, block_count:int=None, query:list=[]):
        for block, is_metarium in self.__listen(direction, block_hash=block_hash, block_count=block_count):
            if not is_metarium:
                continue
            yield block
