import os
from Bio import SeqIO
from ._StreamType import _StreamType as StreamType





class _SeqreadStreamType(StreamType):
    def __init__(self):
        super().__init__(extensions=dict(type(self)._datatypes))
        self._require_qv = True
class SeqreadInStreamType(_SeqreadStreamType):
    _datatypes = {
        '.phd': 'phd',
        '.ab1': 'abi',
    }
    def get_default_data(self):
        return {
            'qv': 0,
            'seq': "",
        }
    def read(self, string):
        y, x = os.path.splitext(string)
        record = SeqIO.read(string, SeqreadInStreamType._datatypes[x])
        ans = dict()
        ans['seq'] = str(record.seq).upper()
        error = None
        try:
            ll = record.letter_annotations['phred_quality']
        except KeyError as exc:
            error = exc
            ans['qv'] = None
        else:
            if len(ll) == 0:
                ans['qv'] = 0
            else:
                ans['qv'] = int(round(sum(ll) / len(ll)))
        if self._require_qv:
            if error is not None:
                raise error
        return ans
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



        

















        






        