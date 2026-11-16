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
import pprint

# My own stuff
from validcombo import test_known_combination
from refstorage import RefStorage, log as refstorage_log
from tools import load_ref_file, average
import  inst_specific as local
from itersheets.itersheets import Reader

# Set up basic logging
#LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)
#refstorage_log = log

# Example call
# python src/sussometer/sussometer.py -i testdata/needscompletion_300k_T.xlsx testdata/verbatim_leg_loc.csv testdata/verbatim_loc.csv


# TODO: EACH TEST* SHOULD RETURN A (DICT) WITH VALUES ONLY FOR THE TESTED BASES


# For easy testing
if __name__ == '__main__':
    print("Testing the susso-o-meter\n")
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", dest="input_file", type=Path, help="input (target) data file")
    ap.add_argument('reference_files', type=Path, nargs="+")
    args = ap.parse_args()
    # Load refence data
    refdata = []
    for fpath in args.reference_files: # Read all reference files
        log.debug(f"Reading reference data file {fpath}.")
        filedata = load_ref_file( fpath ) # Tuple of rows
        refdata.append( RefStorage(filedata) )
            
    # Load data to be processed
    datareader = Reader(args.input_file)
    datareader.open()
    rowcounter = 0
    donecounter = 0
    for rowdict in datareader.dictrows():
        rowcounter += 1
        if local.exclude(rowdict):
            sussvector = {} # No tests performed
            continue # This row should not be analyzed
        for ref in refdata:  # Iterate over reference datasets      
            # output: dictionary with same keys, int = [-1...1] values

            # TODO: we should combine results from various tests SOMEHOW

            sussvector = test_known_combination(rowdict, ref)
            print("suss vector = ", pprint.pformat(sussvector) )
            print("total suss value", average(sussvector, with_zeros=False) )
        # TODO: How should be assign suss values to individual fields in the combo is bad?
        donecounter += 1
    log.info(f"Processed {rowcounter} rows, of which {donecounter} had enough data for analysis.")


