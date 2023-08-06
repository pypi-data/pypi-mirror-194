import lib_dzne_tsv
from ._CharsStreamType import _CharsStreamType
import collections

class TabStreamType(_CharsStreamType):
    def read(self, string, *, strip=False, width=None, strictly=True):
        errors = list()
        lines = type(self).read_lines(file=string)
        header, *rows = (x for x in lib_dzne_tsv.reader(lines))
        for item, count in collections.Counter(header).items():
            if count > 1:
                errors.append(
                    KeyError(
                        f"The column-name {item} occures more than once! "
                    )
                )
        if width is None:
            width = len(header)
        elif width != len(header):
            errors.append(
                ValueError(
                    "The header has the wrong width! "
                )
            )
        for i, row in enumerate(rows):
            diff = len(row) - width
            if diff == 0:
                continue
            if strictly:
                errors.append(
                    ValueError(
                        f"Row {i} has the wrong width! "
                    )
                )
                continue
            if diff > 0:
                row.extend([None] * diff)
            if diff < 0:
                del row[width:]
        if len(errors):
            raise ExceptionGroup(
                "Improperly formatted! ",
                errors,
            )
        df = pd.DataFrame(rows, columns=header)
        if strip:
            df = df.applymap(lambda x: x.strip())
        return df

            
    def write(self, string, data, *, strip=False):
        df = data
        if strip:
            df = df.applymap(lambda x: x.strip())
        rows = [list(df.columns)]
        for i, row in df.iterrows():
            rows.append(list(row))
        with open(string, 'w') as s:
            writer = lib_dzne_tsv.writer(s)
            for row in rows:
                writer.writerow(row)
                