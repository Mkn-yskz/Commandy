# Show all UIDs and records in Vault
# set PYTHONPATH=<absolute path to keepercommander> AWS: /home/ec2-user/environment/Commander:/home/ec2-user/environment/.venv/lib/python3.6/dist-packages
import sys
import os
import getpass
import json
import datetime
from keepercommander import params,api,record

class KeeperSession(params.KeeperParams):
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
        self.user = user or os.getenv(self.__class__.USER) or input(user_prompt)
        self.password = password or os.getenv(self.__class__.PASSWORD) or getpass.getpass(password_prompt)
        api.login(self) # user=self.user, password=self.password)
        api.sync_down(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear_session()  # clear internal variables
    
    def get_every_unencrypted(self):
        for uid, packet in self.record_cache.items():
            yield uid, json.loads(packet['data_unencrypted'].decode('utf-8'))

            
    def get_all_uids(self):
        return self.record_cache.keys()
        
    import datetime
    def get_record(self, uid):
       dt = datetime.datetime.fromtimestamp(self.record_cache[uid]['client_modified_time'] / 1000)
       rec = api.get_record(self, uid)
       rec.modified_time = dt
       return rec
       
       '''
        self.record_uid = record_uid
        self.folder = folder
        self.title = title
        self.login = login
        self.password = password
        self.login_url = login_url
        self.notes = notes
        self.custom_fields = custom_fields or []  # type: list
        self.attachments = None
        self.revision = revision
        self.unmasked_password = None
        self.totp = None
        '''
def print_totp_records():
    with KeeperSession() as keeper_session:
        for uid in keeper_session.get_all_uids():
            record = keeper_session.get_record(uid)
            if record.totp:
                record.modified_time = record.modified_time.isoformat()
                print(json.dumps(record.__dict__, sort_keys=True, indent=4, ensure_ascii=False))

def edit_totp():
    edit_uid = os.getenv('KEEPER_EDIT_UID')
    totp_json = os.getenv('TOTP_JSON')
    with KeeperSession() as keeper_session:
        uids = keeper_session.get_all_uids()
        if edit_uid not in uids:
            print(f"{edit_uid} no in all uids.")
            exit(1)
        record = keeper_session.get_record(edit_uid)
        totp_uri = json_to_totp(totp_json) 
        record.totp = totp_uri
    

import pyotp
def json_to_totp(json_str: str) -> str:
  aotp_dict = json.loads(json_str)
  label_split = aotp_dict['label'].split(':')
  name = label_split[len(label_split) - 1]
  del aotp_dict['label']
  aotp_dict['issuer_name'] = aotp_dict.pop('issuer')
  secret = aotp_dict.pop('secret')
  del aotp_dict['type']
  del aotp_dict['thumbnail']
  del aotp_dict['last_used']
  del aotp_dict['used_frequency']
  del aotp_dict['tags']
  '''
  "type":"TOTP","algorithm":"SHA1","thumbnail":"Default","last_used":1591871947142,"used_frequency":3,"period":30,"tags":[]}
  '''
  return pyotp.utils.build_uri(secret, name, **aotp_dict)
        
if __name__ == '__main__':
    edit_totp()
    exit(0)
