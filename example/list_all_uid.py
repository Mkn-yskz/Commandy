# Show all UIDs in Vault; Set CWD to 'YCommander/example.py' to run this script.
# set PYTHONPATH=<absolute path to keepercommander> AWS: /home/ec2-user/environment/Commander:/home/ec2-user/environment/.venv/lib/python3.6/dist-packages
#sys.path.append("../.venv/lib/python3.6/dist-packages")
import sys
import os
import getpass
import json
import datetime
# sys.path.append("..")  # pwd includes keepercommander"
from keepercommander import params,api,record

class WithParams(params.KeeperParams):
    ''' Login and sync_down automatically 
        user-ID is gotten from $KEEPER_USER
        user password if from $KEEPER_PASSWORD
        or parameters as with(user, password) '''
    USER = 'KEEPER_USER'
    PASSWORD = 'KEEPER_PASSWORD'
  
    
    def get_modified_timestamp(self, record_uid):
        current_rec = self.record_cache[record_uid]
        return current_rec['client_modified_time']
    
    def get_modified_time(self, record_uid):
        return datetime.datetime.fromtimestamp(self.get_modified_timestamp(record_uid) / 1000)

    def __enter__(self, user=None, password=None, user_prompt='User:', password_prompt='Password:'):
        self.user = user or os.getenv(WithParams.USER) or input(user_prompt)
        self.password = password or os.getenv(WithParams.PASSWORD) or getpass.getpass(password_prompt)
        api.login(self) # user=self.user, password=self.password)
        api.sync_down(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear_session()  # clear internal variables
    
    def get_every_unencrypted(self):
        for uid, packet in self.record_cache.items():
            yield uid, json.loads(packet['data_unencrypted'].decode('utf-8'))
 
    def get_every_record(self):
        for uid in self.record_cache:
            yield uid, self.get_record(uid)       
            
    def get_every_uid(self):
        for uid in self.record_cache:
            yield uid
            
    def get_all_uids(self):
        return self.record_cache.keys()
        
    import datetime
    def get_record(self, uid):
       dt = datetime.datetime.fromtimestamp(self.record_cache[uid]['client_modified_time'] / 1000)
       rec = api.get_record(self, uid)
       rec.modified_time = dt
       return rec


if __name__ == '__main__':
    import logging
    from operator import attrgetter
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.INFO)
    with WithParams() as keeper_session:
        rec_list = []
        for uid in keeper_session.get_all_uids():
            rec_list.append(keeper_session.get_record(uid))
        rec_list.sort(key=attrgetter('modified_time', 'title'))
        for rr in rec_list:
            rr_dict = rr.__dict__
            rr_dict['modified_time'] = rr.modified_time.isoformat()
            rr_d = {k:v for k,v in rr_dict.items() if v is not None} # remove null value item
            print(json.dumps(rr_d, sort_keys=True, indent=4, ensure_ascii=False))
        
    exit(0)
