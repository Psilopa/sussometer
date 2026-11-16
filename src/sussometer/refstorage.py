import logging
log = logging.getLogger(__name__)
import pprint

# Use a database here?
class RefStorage():
    def __init__(self:Self, data: Sequence[str, ...]):
        """"Input data = a sequence of (data1,data2,..., suss value, N ).

        First line=field names"""
        self._fields = tuple(data[0][:-2]) # First line excep
        self._data = tuple(data[1:]) # Data lines: skip the N_datapoints        
        log.debug(f"refStorage self.fields: {self.fields}")
        pprint.pp(self._fields)
        # list of (data1, ...), suss_value pairs
        suss_col_ind = -2 # 2nd from the right
        tmpind = zip(tuple(x[:suss_col_ind] for x in self._data),
                          [float(x[suss_col_ind]) for x in self._data] )
        log.debug(f"1st data row = {self._data[0]}" )
        # dictionary of (data1, data1) -> suss_value
        self.index = {k:v for k,v in tmpind}
        del self._data # May want to expose this later

    @property
    def fields(self:Self) -> tuple[str]: 
        return self._fields 
    
    def getsuss(self:Self,datatuple) -> float:
        return self.index.get(datatuple,None)

