# This is suss
# Suss values rank from +1 (probably ok) to 0 (unknown) to -1 (probably bad)
# Input: dictionary key:value_that_can_be_converted_to_string

# STdlib
import json
import logging

# My own stuff
from validcombo import test_known_combinations
from testdata import *
from refstorage import RefStorage, log as refstorage_log
from tools import jaccard
from inst_specific import extract_alltext

# Set up basic logging
#LOGLEVEL = logging.DEBUG
LOGLEVEL = logging.INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=LOGLEVEL)
log = logging.getLogger(__name__)
refstorage_log = log

# output: dictionary with same keys, int = [-1...1] values
# Reference data:
#{} -> correctness_index
reference1 = [ ("verbatim_locality", "verbatim_collector", 0),
               ("U. Nurmijarvi", "M. Koponen", 1) ,
               ("U. Murmijarvi", "M. Koponen", -0.25) ,
               ("U. Murnijarvi", "M. Koponen", -0.5) ,
             ]

# For easy testing
if __name__ == '__main__':    
    d = json.loads(json1)       
    ref1 = RefStorage(reference1)
    values = test_known_combinations(d, ref1)

    # Should be keep track of all individual values and do a weighted sum at the end?
    print("suss value = ",values )
    # SOme testing
    print("alltext =", extract_alltext(d))
    print("jaccard =", jaccard(json1, json2) )

