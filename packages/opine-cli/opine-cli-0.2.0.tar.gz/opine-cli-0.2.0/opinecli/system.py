import requests
import json
import tabulate
import pandas as pd
from opinecli.config import ConfigUtils
from opinecli.project import ProjectUtils

class System(object):
    def __init__(self):
        self.__config_utils = ConfigUtils()

    
    def stats(self):
        """ Get system stats"""
        config_data = self.__config_utils.get()
        params = {}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/system/stats', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        print()

    def users(self):
        """ Get stat of all users"""
        config_data = self.__config_utils.get()
        params = {}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/users/stats', json=params, headers=headers)
        print(result)
        # print()
        # print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        # print()

    