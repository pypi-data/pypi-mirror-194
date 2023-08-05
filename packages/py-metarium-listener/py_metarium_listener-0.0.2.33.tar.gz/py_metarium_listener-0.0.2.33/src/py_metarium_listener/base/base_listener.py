from py_metarium_decoder import Decoder


class BaseListener:

    def __init__(self, url=None) -> None:
        self.__decoder = Decoder(url)
    
    def decoder(self):
        return self.__decoder
    
    def info(self):
        return self.__decoder.info()

    def listen(self, direction:str, block_hash:str=None, block_count:int=None, query:list=[]):
        raise NotImplementedError
