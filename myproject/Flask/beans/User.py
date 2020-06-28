from api import authn
import json

import logging
# from service import controller

logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

RS_URL = 'https://us-4.rightscale.com/'


class User1:
    bearer_token = ''

    def __init__(self, rs_token):
        self.rs_token = rs_token
        self.RS_URL = 'https://us-4.rightscale.com/'
        self.bearer_token

    def display_rs_token(self, rs_token):
        logging.info("Inside display_rs_token method.")
        print(rs_token)
        return rs_token

    def authenticate_user(self, rs_token):
        access_token = authn.authn_to_RS(self.RS_URL, rs_token)
        if access_token.status_code != 200:
            return access_token
        my_json = access_token.content.decode('utf8').replace("'", '"')
        br_token = json.loads(my_json)['access_token']
        self.bearer_token = br_token
        return access_token

    def test_method(self):
        print(self.rs_token)
