"""
json_to_csv import format converter
"""
import sys
import json
import  csv
import io
from typing import Dict, List, Optional

def dict_to_list(top_dict: Dict[str, str]) -> List[Optional[str]]:
    records = top_dict['records']
    rec = records[0]
    custom_fields = []
    for k, v in rec['custom_fields'].items():
      custom_fields += [k, v]
    folder_dict =  rec['folders'][0]
    folder_name = folder_dict['folder']
    rec0 = [
        folder_name,
        rec['title'],
        rec['login'],
        rec['password'],
        rec['login_url'],
        rec['notes'],]
    return rec0 + [None] + custom_fields

def json_to_csv(js: str) -> str:
    outp = io.StringIO()
    top_dict = json.loads(str)
    js_list = dict_to_list(top_dict)
    writer = csv.writer(outp, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(js_list)
    retval = outp.getvalue()
    return retval
    
in_f = sys.argv[0]
with open(in_f) as in_f:
    top_dict = json.loads(in_f.read())
    records = top_dict['records']
    rec = records[0]
    custom_fields = []
    for k, v in rec['custom_fields'].items():
      custom_fields += [k, v]
    folder_dict =  rec['folders'][0]
    folder_name = folder_dict['folder']
    rec0 = [
        folder_name,
        rec['title'],
        rec['login'],
        rec['password'],
        rec['login_url'],
        rec['notes'],]
    rec1 = rec0 + [None] + custom_fields
    print(','.join(rec1))