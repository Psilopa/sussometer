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

decimals = 3 # Round to X decimals
def average(sussdict:SussVector, weights:None|Sequence[str|int]=None, with_zeros=True):
    if not with_zeros: data = tuple(x for x in sussdict.values() if x)
    else: data = sussdict.values() 
    if len(data) == 0: return 0.0 # all values were zero and with_zeros=False)
    if not weights: return round( statistics.mean( data ), decimals)
    else:
        assert len(data) == len(weights) # TODO: Should raise an Error
        valsum = sum(g*val for (g, val) in zip(weights, data) )
        return round( valsum / sum(weights) , decimals)
