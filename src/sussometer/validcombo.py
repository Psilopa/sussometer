        
def test_known_combinations(data:dict[str:Any],
                            *args: Sequence) -> dict[str,floar]:
    sus = {k:0 for k in data.keys()} # Default to zero for all fields
    for ref in args:
        #Combo of fields to test
        totest = tuple(data[x] for x in ref.fields)
        val = ref.getsuss(totest)
        # TODO: How should be assign suss values to individual fields in the combo is bad?
        sus.update( {k:val for k in ref.fields} )
    return sus        
