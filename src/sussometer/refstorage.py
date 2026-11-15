import logging
log = logging.getLogger(__name__)

# Use a database here?
class RefStorage():
    def __init__(self:Self, data: Sequence[str, ...]):
        """"Input data = a sequence of (data1,data2,..., suss value ).

        First line=field names"""
        self._fields = tuple(data[0][:-1])
        self._data = tuple(data[1:])
        log.debug(f"refStorage self.fields: {self.fields}")
        # list of (data1, data1), suss_value pairs
        tmpind = zip(tuple(x[:-1] for x in self._data),
                          [float(x[-1]) for x in self._data] )
        # dictionary of (data1, data1) -> suss_value
        self.index = {k:v for k,v in tmpind}
        del self._data # May want to expose this later
    @property
    def fields(self:Self) -> tuple[str]: return self._fields 
    
    def getsuss(self:Self,datatuple) -> float:
        "Returns a dicionary mapping column_name: suss_value."
        return self.index.get(datatuple,0.0)

