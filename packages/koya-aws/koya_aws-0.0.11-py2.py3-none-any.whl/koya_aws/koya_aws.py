import os
import re
import io
import datetime
import pandas as pd

def get_latest_file_aws(available_files,source):

    """Get the latest file for a source from the list of available files.

    This function filters the list of available files by checking if the source string
    is in the file name. The filtered files are then sorted by date and the latest file
    is returned.

    :param available_files: List of strings containing the names of the available files
    :param source: String to match with the available files to get the latest file
    :return: String with the name of the latest file or None if no match is found.
    :raises: ValueError if no file is found for the specified source.
    """

    files = [k for k in available_files if (source in k) and ("______" in k)]
    
    if len(files) == 0:
        files = [k for k in available_files if (source in k)]
    
    if len(files)==0:
        raise ValueError(f'file not found for source: {source}')

    l=[]
    for k in files:
        d=re.search('(\d{2})-(\d{2})-(\d{4})',k)
        if d:
            date = f"{d.group(1)}-{d.group(2)}-{d.group(3)}"
            l.append((k,pd.Timestamp(date)))
            
    l=(sorted(l, key = lambda x: x[1]))
    latest = l[-1][0]
    if source not in latest:
        return None
    return latest