def extract_alltext(jsondata):
    outblock = jsondata["verbatim_all_text"]
    return " ".join( [d["verbatim_text"] for d in outblock] )
        
