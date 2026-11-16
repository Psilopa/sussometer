"""
Generate sussometer reference files from verified Kotka XLSX sheets.

CSV Format uses the Excel detail output format but assumes UTF-8 encoding:
fieldname1 [, fieldname2, ...], N-of-data-points, suss-value

"""

#STDLIB
import sys
import re
import json
import difflib
import pprint
import tomllib
from pathlib import Path

# My own packages
from itersheets import itersheets

def data_from_AI_output(rowdict):
    cell = rowdict[ai_output_field]
    if not cell: return {}
    try:
        d = json.loads( cell )    
        return json.loads(d[ ai_content_key ])
    except json.decoder.JSONDecodeError:
        return {}

    
def valid_as_ref(rowdict) -> None:
    "Check of this row is good enough for a refernce. Raises a RefDataError on failure."
    if not quality_field_name in rowdict.keys():
        raise RefDataError(f"No field '{quality_field_name}' on row.")
    quality_val = rowdict[quality_field_name]
    if not quality_val or (not good_enough_marker in quality_val):
        RefDataError(f"Missing marker '{good_enough_marker}' on row.") 
    # By default, accept


class RefDataError(ValueError): pass


text_minlength = 4 # Any string with this length can be compared on its own
def extract_ref_from_Kotka_file(fp:Path,
                                fields:Sequence[str,...],
                                cmpfunc:Callable):
    infile = itersheets.Reader( fp ) # Generic reader guesses the type from the file name
    infile.open()
    outrows = []
    for d in infile.dictrows():
        try:
            valid_as_ref(d) # Raises an error on failure
            aidata = data_from_AI_output(d)
            if not aidata: RefDataError(f"Could not read aidata.") 
            ai = []
            ok = []
            for field in fields:
                aivalue = aidata.get(field,"") or ""
                # If any value too short, do not compare at all
                if len(aivalue) < text_minlength :
                    raise RefDataError(f"Value '{aivalue}' too short, will now use this row.") 
                # is the text long enough for comparison
                ai.append( aivalue )
                ok.append(d.get(field,"") or "" )
            # Locality on it own
            suss = cmpfunc(ai,ok)
            outrow = (tuple(ai), suss)
            outrows.append(outrow)
        except RefDataError as msg:
            #log.debug(f"Skipping row, reason: {msg}")            
            # Some data did not 
            pass
    infile.close()
    return outrows


def handle_duplicates(outrows, cap_maxval = 5):
    """Convert rows to a dictionary. In case of duplicates, combines suss values.

    The test version sums the suss values. Finally, they are divided with the
    in set maximum
    """
    outdict = {}
    maxval = 0 # LArgest absolute value in dataset
    # To save memory, delete from outrows as we go?
    for index, suss in outrows:
        # First data point with this index
        if index not in outdict: outdict[index] = (suss, 1)
        else:
            # One solution: add old and new suss values.
            # This means positives can cancel out negatives
            suss = float( outdict[index][0] ) + float(suss) # old  + new
            suss = min( suss , cap_maxval ) # Cap suss at cap_maxval_at top
            suss = max( suss , -cap_maxval ) # Cap suss at cap_maxval_at negative side
            maxval = max( abs(suss), maxval )
            # Return 
            outdict[index] = (suss, #  Suss value
                              outdict[index][1] +  1   # number of records with this index
                              ) 
                              
    # Finally, normalize in a primitive way: linear scaling to abs(maxval) = 1
    for k,v in outdict.items():
        outdict[k] = ( float(v[0]/maxval), v[1] )
    return outdict


def cmpstring(ai:Sequence,ok:Sequence, ignorechars = [r"\n",r"\t"], combinespaces = True) -> float|int:
    """Compare string by strict match.

    Keywords:
	ignorechars: these characters will be deleted from the string before comparison. Uses regexp escapes.
        combinechars: a list of regular expressions 
	"""
    re_spaces = r"\s+"
    assert len(ai) == len(ok)    
    for x,y in zip(ai,ok):
        if combinespaces:
            x = re.sub(re_spaces, " ", x)
            y = re.sub(re_spaces, " ", y)
        for c in ignorechars:
            x = re.sub(c, "", x)
            y = re.sub(c, "", y)
        if x.lower() != y.lower(): return -1
    return 1 # If we did not fail, we succeesed

def outfile_format(orignal, fields, template):
    op = Path(orignal)
    stem = op.stem + template % "_".join(fields)
    outp = op.with_stem(stem)
    return outp
    

def extract(fields, fp, conf):
    # Extract 1
    outrows = extract_ref_from_Kotka_file(fp,  fields, cmpstring)
    outdict = handle_duplicates(outrows, cap_maxval = conf["output"]["cap_maxval_at"] )
    header = fields + ("sussvalue","n_datapoints")
    oftempalate = conf["output"]["output_file_naming"]
    outfilename = outfile_format(fp, fields, oftempalate)
    print("outfilename = ", outfilename)
    outf = itersheets.Writer(outfilename)
    outf.open("w",header)
    for (k,v) in outdict.items():
        outrow = k + v
        od = {k:v for k,v in zip(header, outrow)}
#        pprint.pp(od)
        outf.add_row_from_dict(od,
                               itersheets.new_column_action.INSERT
                               )
    outf.close()


# ------------------ main ---------------------
if __name__ == '__main__':
    with open("tools/ref_setup.toml", "rb") as f:
        conf = tomllib.load(f)
    pprint.pp(conf)
    fp = sys.argv[1]
    #Parameters
    global ai_output_field
    global quality_field_name
    global ai_content_key
    global good_enough_marker
    ai_output_field = conf["input"]["ai_output_field"]
    ai_content_key = conf["input"]["ai_content_key"]
    quality_field_name = conf["input"]["quality_field_name"]
    good_enough_marker = conf["input"]["good_enough_marker"]
    for n in conf["fields"].keys():
        fields = tuple(conf["fields"][n]['fieldnames'])
        extract(fields, fp, conf)

