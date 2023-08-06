import tempfile
from ._StreamType import _StreamType as StreamType

class _CharsStreamType(StreamType):
    def data_to_str(self, data):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfile = os.path.join(tmpdir, 'a')
            self.write(tmpfile, data)
            with open(tmpfile, 'r') as s:
                return s.read() 
    def read_lines(file):
        lines = list()
        with open(file, 'r') as s:
            for line in s:
                assert line.endswith('\n')
                lines.append(line[:-1])
        return lines
    def write_lines(file, lines):
        with open(file, 'w') as s:
            for line in lines:
                print(line, file=s)
