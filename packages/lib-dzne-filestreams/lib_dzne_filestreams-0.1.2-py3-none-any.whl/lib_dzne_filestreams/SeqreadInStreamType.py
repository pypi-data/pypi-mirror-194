import os
from Bio import SeqIO
from ._SeqreadStreamType import _SeqreadStreamType


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

