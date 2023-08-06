import lib_dzne_basetables
from ._CharsStreamType import _CharsStreamType


class BASEStreamType(_CharsStreamType):
    def __init__(self, basetype=None):
        self._basetype = basetype
        if basetype is None:
            x = None
        elif basetype in {'a', 'd', 'm', 'y', 'c'}:
            x = {f".{basetype}base": f"{basetype}base"}
        else:
            raise ValueError()
        super().__init__(extensions=x)
    def get_default_data(self):
        return lib_dzne_basetables.table.make(basetype=self._basetype)
    def read(self, string):
        data = lib_dzne_tsv.from_file(string)
        try:
            data = lib_dzne_basetables.table.make(data, basetype=self._basetype)
        except BaseException as exc:
            raise ValueError(f"The BASE-table {ascii(string)} violates the standards! ") from exc
        return data
    def write(self, string, data):
        lib_dzne_basetables.table.check(data, basetype=self._basetype)
        lib_dzne_tsv.to_file(string, data) 
