# Show all UIDs in Vault
import os
import getpass
from keepercommander import api, params # set PYTHONPATH=<absolute path to keepercommander>


class KeeperLogin(object):
    ''' Login and sync_down automatically 
        user-ID is gotten from $KEEPER_USER
        user password if from $KEEPER_PASSWORD
        or parameters as with(user, password) '''

    USER = 'KEEPER_USER'
    PASSWORD = 'KEEPER_PASSWORD'

    def __enter__(self, user=None, password=None, user_prompt='User:', password_prompt='Password:'):
        self.params = params.KeeperParams()
        self.params.user = user or os.getenv(KeeperLogin.USER) or input(user_prompt)
        self.params.password = password or os.getenv(KeeperLogin.PASSWORD) or getpass.getpass(password_prompt)
        api.login(self.params)
        api.sync_down(self.params)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.params.clear_session()  # clear internal variables
