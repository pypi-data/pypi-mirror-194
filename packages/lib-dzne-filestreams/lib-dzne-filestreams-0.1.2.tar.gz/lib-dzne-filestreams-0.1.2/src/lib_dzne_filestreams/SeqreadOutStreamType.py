import os
from Bio import SeqIO
from ._SeqreadStreamType import _SeqreadStreamType


class SeqreadOutStreamType(_SeqreadStreamType):
    _datatypes = {
        '.phd': 'phd',
    }
    def write(self, string, data):
        data = dict(data)
        y, x = os.path.splitext(string)
        record = SeqRecord(data.pop('seq'))
        record.letter_annotations['phred_quality'] = [data.pop('qv')] * len(record.seq)
        if len(data):
            raise ValueError()
        SeqIO.write(string, SeqreadInStreamType._datatypes[x], record)
    def data_to_str(self, data):
        return data.__repr__



        

















        






        