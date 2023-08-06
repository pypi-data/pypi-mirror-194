import os
from ._StreamType import _StreamType


class ResourceStreamType(_StreamType):
    def __init__(self, streamType):
        super().__init__()
        self._streamType = streamType
    @property
    def streamType(self):
        return self._streamType
    def read(self, string):
        files = list()
        if string in ("", '-'):
            files.append(string)
        elif os.path.isfile(string):
            files.append(string)
        elif os.path.isdir(string):
            for root, dirnames, filenames in os.walk(string):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            raise ValueError()    
        return [self._streamType(file) for file in files]     
