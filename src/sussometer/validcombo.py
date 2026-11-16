from sussvector import SussVector
from refstorage import RefStorage

decimals = 3
def test_known_combination(data:dict[str:Any],
                           ref:RefStorage
                           ) -> SussVector:
    # Extract combo of fields to test from dataa
    totest = tuple(data[x] for x in ref.fields)
    sussvalue = ref.getsuss(totest)
    return SussVector( {k:round(sussvalue, decimals) for k in ref.fields if sussvalue} ) # Set all fields on this combination to the received sussvalue



