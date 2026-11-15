from refstorage import RefStorage

def test_known_combination(data:dict[str:Any],
                           ref:RefStorage
                           ) -> dict[str,floar]:
    # type of 
    # Default to zero for all fields that can be tested with ref
    sus = {k:0 for k in ref.fields} 
    # Extract combo of fields to test from dataa
    totest = tuple(data[x] for x in ref.fields)
    # Test
    val = ref.getsuss(totest)    
    # TODO: How should be assign suss values to individual fields in the combo is bad?
    sus.update( {k:val for k in ref.fields} )
    return sus        

        
def test_known_combinations(data:dict[str:Any],
                            *args: Sequence[RefStorage]
                            ) -> dict[str,floar]:
    sus = {} 
    for ref in args:
        susx = test_known_combination(data, ref)
        # TODO: HOW DO WE COMBINE SUS SCORES
        sus.update(susx) # NOT A GOOD SOLUTION
    return sus        
