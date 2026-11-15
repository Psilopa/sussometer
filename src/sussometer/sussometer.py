# This is suss
# Suss values rank from +1 (probably ok) to 0 (unknown) to -1 (probably bad)
# Input: dictionary key:value_that_can_be_converted_to_string

# stdlib
import json
import logging
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

# Set up basic logging
#LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)
#refstorage_log = log

# output: dictionary with same keys, int = [-1...1] values

# Example call
# python src/sussometer/sussometer.py -i testdata/needscompletion_300k_T.xlsx testdata/locality_collector.csv 

# For easy testing
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", dest="input_file", type=Path, help="input (target) data file")
    ap.add_argument('reference_files', nargs="+")
    args = ap.parse_args()
    refdata = []
    for fn in args.reference_files:
        filedata = load_ref_file( Path(fn) ) # Tuple of rows
        refdata.append( RefStorage(filedata) )
        
    d = json.loads(json1)
    print(d["verbatim_locality"])
    print(d["verbatim_collector"])
    values = test_known_combinations(d, *refdata)

    # Should be keep track of all individual values and do a weighted sum at the end?
    print("suss value = ",values )
    # SOme testing
    print("alltext =", extract_alltext(d))
    print("jaccard =", jaccard(json1, json2) )

