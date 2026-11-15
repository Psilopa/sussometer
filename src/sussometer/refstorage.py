import logging
log = logging.getLogger(__name__)

# Use a database here?
class RefStorage():
    def __init__(self,data):
        self._fields = data[0][:-1]
        self.data = data[1:]
        log.debug(f"refStorage self.fields: {self.fields}")
        tmpind = zip([x[:-1] for x in self.data],
                          [x[-1] for x in self.data])
        # Map header fields to data rows
        self.index = {k:v for k,v in tmpind}
    @property
    def fields(self): return self._fields
    
    def getsuss(self,x):
        return self.index.get(x,1.5) # Defaults to 0.0 (no opinion)

