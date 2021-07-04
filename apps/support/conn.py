import requests
from requests.auth import HTTPBasicAuth

import core.config

class JitBitAPI:

    def __init__(self):
        self.auth = HTTPBasicAuth(core.config.HELPDESK_USER, core.config.HELPDESK_PWD)

        if not self.test_creds():
            raise ValueError("Authorization failed, please check your credentials")
        else:
            print('Connection to Arizona Pipeline JitBit Established')

    def test_creds(self):
        """
        Ensure a connection to the JitBit API
        """
        response = self._get_request("Authorization")
        return response.status_code == 200

    def _get_request(self, method):
        """
        Default method for JitBit API calls
        """
        url = f'{core.config.HELPDESK_URL}/api/{method}'
        return requests.get(url, auth=self.auth)

    def _post_request(self, method):
        """
        Default method for JitBit API POSTS
        """
        url = f'{core.config.HELPDESK_URL}/api/{method}'
        return requests.post(url, auth=self.auth)