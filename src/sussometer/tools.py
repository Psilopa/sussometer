
def jaccard(text1, text2):
    assert len(text1) != 0
    assert len(text2) != 0
    t1 = set(text1.split(" "))
    t2 = set(text2.split(" "))
    u = len( t1.union(t2) )
    i = len( t1.intersection(t2) )
    return i/float(u)
