import tomllib
import tomli_w
from ._CharsStreamType import _CharsStreamType

class TOMLStreamType(_CharsStreamType):
    def __init__(self):
        super().__init__(extensions={'.toml': "TOML"})
    def get_default_data(self):
        return dict()
    def read(self, string):
        with open(string, 'rb') as s:
            return tomllib.load(s)
    def write(self, string, data):
        with open(string, 'wb') as s:
            tomli_w.dump(data, s)