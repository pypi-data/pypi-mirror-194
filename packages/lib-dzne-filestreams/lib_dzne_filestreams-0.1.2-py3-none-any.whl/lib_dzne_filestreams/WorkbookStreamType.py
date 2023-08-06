import openpyxl
import lib_dzne_workbook
from ._StreamType import _StreamType as StreamType



class WorkbookStreamType(StreamType):
    def __init__(self):
        super().__init__(extensions={'.xlsx':'excel'})
    def get_default_data(self):
        return openpyxl.Workbook()
    def read(self, string):
        return lib_dzne_workbook.from_file(string)
    def write(self, string, data):
        if type(data) is not openpyxl.Workbook:
            raise TypeError()
        data.save(filename=string)