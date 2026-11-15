# This is suss
# Suss values rank from +1 (probably ok) to 0 (unknown) to -1 (probably bad)
# Input: dictionary key:value_that_can_be_converted_to_string

# stdlib
import json
import logging
import statistics
# for main
import sys
import argparse
from pathlib import Path

# My own stuff
from validcombo import test_known_combinations
from testdata import *
from refstorage import RefStorage, log as refstorage_log
from tools import jaccard, load_ref_file
from inst_specific import extract_alltext
import pprint

# Set up basic logging
#LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)
#refstorage_log = log

def average(sussdict:dict[str,int|float], weights:None|Sequence[str|int]=None):
    assert len(sussvector) > 0, "Cannot average an empty list." 
    if not weights: return statistics.mean( sussvector.values() ) 
    else:
        assert len(sussvector) == len(weights) # TODO: Should raise an Error
        return sum(g*val for (g, val) in zip(weights, sussvector.values())) / sum(weights)
    return 2

# Example call
# python src/sussometer/sussometer.py -i testdata/needscompletion_300k_T.xlsx testdata/locality_collector.csv 


# TODO: EACH TEST* SHOULD RETURN A (DICT) WITH VALUES ONLY FOR THE TESTED BASES


# For easy testing
if __name__ == '__main__':
    print("Testing the susso-o-meter\n")
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", dest="input_file", type=Path, help="input (target) data file")
    ap.add_argument('reference_files', nargs="+")
    args = ap.parse_args()
    refdata = []
    for fn in args.reference_files:
        filedata = load_ref_file( Path(fn) ) # Tuple of rows
        refdata.append( RefStorage(filedata) )
        
    d = json.loads(json1)
    d["verbatim_locality"] = "U. Murmijärvi" # Set for testing
#    print(d["verbatim_collector"])
    # output: dictionary with same keys, int = [-1...1] values
    sussvector = test_known_combinations(d, *refdata)
    print("suss vector = ", pprint.pformat(sussvector) )
    print("total suss value", average(sussvector) )

    # Should be keep track of all individual values and do a weighted sum at the end?
    # SOme testing
    print("alltext =", extract_alltext(d))
    print("jaccard =", jaccard(json1, json2) )

