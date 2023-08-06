import os

class _StreamType:
    class FileExtensionError(ValueError):
        pass
    class _Stream:
        @property
        def streamType(self):
            return self._streamType
        @property
        def ext(self):
            return os.path.splitext(self._string)
        def __str__(self):
            return self._string
        def read(self):
            if self._string == "":
                return self._streamType.get_default_data()
            if self._string == "-":
                return self._streamType.read_stdin()
            #if not os.path.isfile(self._string):
            #    raise FileNotFoundError()
            return self._streamType.read(self._string)
        def write(self, data, overwrite=False):
            if self._string == "":
                # quiet
                return
            if self._string == "-":
                print(self._streamType.data_to_str(data))
                return
            if os.path.isdir(self._string):
                raise NotImplementedError()
            #self._streamType._fits(string)
            if os.path.exists(self._string) and not overwrite:
                raise IOError()
            self._streamType.write(self._string, data)
    def __call__(self, string):
        if type(string) is not str:
            raise TypeError(f"Streams can only be created from strings! The type {type(string)} is not supported! ")
        if string not in ("", '-') and self._extensions is not None:
            y, x = os.path.splitext(string)
            if x not in self._extensions.keys():
                raise _StreamType.FileExtensionError(f"{ascii(string)}: {ascii(x)} not among {tuple(self._extensions.keys())}! ")
        #stream = type(self)._Stream()
        stream = _StreamType._Stream()
        stream._streamType = self
        stream._string = string
        return stream
    def __init__(self, *, extensions=None):
        self._extensions = dict(extensions) if (extensions is not None) else None
    def get_default_data(self):
        raise NotImplementedError()
    def read_stdin(self):
        raise NotImplementedError()
    def read(self, string):
        raise NotImplementedError()
    def data_to_str(self, data):
        return data.__repr__()
    def write(self, string, data):
        raise NotImplementedError()
        
 
