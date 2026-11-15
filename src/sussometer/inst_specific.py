import logging
log = logging.getLogger(__name__)

def extract_alltext(rowdict:dict[str:Any]) -> str:
    "Extract the alltext verbatim field"    
    return rowdict.get("verbatim_all_text", "")        

def exclude(rowdict:dict[str:Any]) -> bool:
    "Check if the row has enough data to be analyzed."
    alltext = extract_alltext(rowdict)
    if alltext: log.debug(f"alltext ='{repr(alltext)}'" )
    if not alltext or len(alltext) < 4:  # Only a few characters
        return True
    return False
    
