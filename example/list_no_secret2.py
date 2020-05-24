# Show all UIDs in Vault
import sys
import os
import getpass
import json
#sys.path.append(".")  # pwd includes keepercommander"
#sys.path.append("../.venv/lib/python3.6/dist-packages")
from keepercommander import api, params # set PYTHONPATH=<absolute path to keepercommander>
from keeper_login import KeeperLogin

with KeeperLogin() as keeper_login:
    for uid, packet in keeper_login.params.record_cache.items():
        record = api.get_record(keeper_login.params, uid) 
        data = json.loads(packet['data_unencrypted'].decode('utf-8'))
        if 'secret2' not in data: #, '<Nil>') == '<Nil>':
            print(f"'secret2' is None at {uid}")
            record.display(params=keeper_login.params)

exit(0)
