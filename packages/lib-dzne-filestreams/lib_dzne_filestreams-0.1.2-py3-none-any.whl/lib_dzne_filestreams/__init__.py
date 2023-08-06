import os
from .TOMLStreamType import TOMLStreamType
from .WorkbookStreamType import WorkbookStreamType
from .BASEStreamType import BASEStreamType
from .TextStreamType import TextStreamType
from .SeqreadInStreamType import SeqreadInStreamType
from .SeqreadOutStreamType import SeqreadOutStreamType
from .ResourceStreamType import ResourceStreamType




def walk(resources):
    for resource in resources:
        if resource in ("", '-'):
            yield resource
        elif os.path.isfile(resource):
            yield resource
        elif os.path.isdir(resource):
            for root, dirnames, filenames in os.walk(resource):
                for filename in filenames:
                    yield os.path.join(root, filename)
        else:
            raise ValueError()






        

















        






        