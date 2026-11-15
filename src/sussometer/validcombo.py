from refstorage import RefStorage

def test_known_combination(data:dict[str:Any],
                           ref:RefStorage
                           ) -> dict[str,floar]:
    # type of 
    # Default to zero for all fields that can be tested with ref
    sus = {k:0 for k in ref.fields} 
    # Extract combo of fields to test from dataa
    totest = tuple(data[x] for x in ref.fields)
    val = ref.getsuss(totest)    
    sus.update( {k:val for k in ref.fields} )
    return sus        


