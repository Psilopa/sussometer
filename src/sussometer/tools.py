from pathlib import Path
from itersheets.itersheets import Reader



def jaccard(text1:str, text2:str) -> float:
    assert len(text1) != 0
    assert len(text2) != 0
    t1 = set(text1.split(" "))
    t2 = set(text2.split(" "))
    u = len( t1.union(t2) )
    i = len( t1.intersection(t2) )
    return i/float(u)

def load_ref_file(filepath:Path) -> tuple[str,...]:
    r = Reader(filepath)
    r.open()
    data = [r.fields]
    for d in r.tuplerows():
        data.append(d)
    return tuple(data)
