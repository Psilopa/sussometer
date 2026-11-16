"""
Generate sussometer reference files from verified Kotka XLSX sheets.

CSV Format uses the Excel detail output format but assumes UTF-8 encoding:
fieldname1 [, fieldname2, ...], N-of-data-points, suss-value

"""

import sys
import json
import pprint
import difflib
from itersheets import itersheets

ai_output_field = "raw"
ai_content_key = "output_text"
def data_from_AI_output(rowdict):
    field = rowdict[ai_output_field]
    if not field:
        return {}
    d = json.loads( field )    
    return json.loads(d[ ai_content_key ])
    
good_enough_marker = "GX.19333"
def valid_as_ref(rowdict) -> bool:
    "Check of this row is good enough for a refernce"
    qualityfield = rowdict["check"] # Note, this is not standard
    if not qualityfield: return False
    if good_enough_marker in qualityfield: return True
    return False # By default, fail

text_minlength = 5 # Any string with this length can be compared on its own
def extract_ref_from_Kotka_file(fp:Path,
                                fields:Sequence[str,...],
                                cmpfunc:Callable):
    infile = itersheets.Reader( fp ) # Generic reader guesses the type from the file name
    infile.open()
    outrows = []
    for d in infile.dictrows():
        # Check if valid as
        if not valid_as_ref(d): continue
        aidata = data_from_AI_output(d)
        ai = []
        ok = []
        for field in fields:
            tmpai = aidata.get(field,"") or ""
            # is the text long enough for comparison
            if len(tmpai) < text_minlength: continue 
            ai.append( tmpai )
            ok.append(d.get(field,"") or "" )
        # Locality on it own
            suss = cmpfunc(ai,ok)
            n_values = 394384
            outrow = (tuple(ai), suss)
            outrows.append(outrow)
    infile.close()
    return outrows

def handle_duplicates(outrows):
    """Convert rows to a dictionary. In case of duplicates, combines suss values.

    The test version sums the suss values. Finally, they are divided with the
    in set maximum
    """
    outdict = {}
    maxval = 0
    cap_maxval_at = 3
    # To save memory, delete from outrows as we go?
    for index, suss in outrows:
        # First data point with this index
        if index not in outdict: outdict[index] = (suss, 1)
        else:
            # One solution: add old and new suss values
            suss = float( outdict[index][0] ) + float(suss) # old  + new
            maxval = max( abs(suss), maxval )
            # Cap suss at cap_maxval_at
            suss = min( outdict[index][0] + suss, cap_maxval_at )
            # Return 
            outdict[index] = (suss,  outdict[index][1] +  1 )
                              
    # Finally, normalize in some way
    for k,v in outdict.items():
        outdict[k] = ( float(v[0]/maxval), v[1] )
    return outdict

def cmpfunc(ai:Sequence,ok:Sequence) -> float|int :
    "Compare string by strict match"
    assert len(ai) == len(ok)
    for x,y in zip(ai,ok):
        if x.lower() == y.lower(): return 1
        return -1

if __name__ == '__main__':
    fp = sys.argv[1]
    # Extract 1
    fields = ("verbatim_collector",)
    outrows = extract_ref_from_Kotka_file(fp,  fields, cmpfunc)
    outdict = handle_duplicates(outrows)
    header = fields + ("sussvalue","n_datapoints")
    outf = itersheets.Writer("verbatim_collector.csv", encoding="utf8")
    outf.open("w",header)
    for (k,v) in outdict.items():
        outrow = k + v
        od = {k:v for k,v in zip(header, outrow)}
        outf.add_row_from_dict(od,
                               itersheets.new_column_action.INSERT
                               )
    outf.close()


