from pathlib import Path
from itersheets.itersheets import Reader
import statistics

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

def average(sussdict:dict[str,int|float], weights:None|Sequence[str|int]=None):
    assert len(sussdict) > 0, "Cannot average an empty list." 
    if not weights: return statistics.mean( sussdict.values() ) 
    else:
        assert len(sussdict) == len(weights) # TODO: Should raise an Error
        return sum(g*val for (g, val) in zip(weights, sussdict.values())) / sum(weights)
    return 2
