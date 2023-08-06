from ._CharsStreamType import _CharsStreamType

class TextStreamType(_CharsStreamType):
    def __init__(self):
        super().__init__(extensions={'.log': 'Log', '.txt': 'Text'})
    def get_default_data(self):
        return list()
    def read(self, string):
        return type(self).read_lines(file=string)
    def write(self, string, data):
        type(self).write_lines(file=string, lines=data)
 
