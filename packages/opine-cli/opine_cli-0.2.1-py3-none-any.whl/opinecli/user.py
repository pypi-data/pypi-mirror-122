import requests
import json
import tabulate
import pandas as pd
from opinecli.config import ConfigUtils
# from opinecli.project import ProjectUtils

class User(object):
    def __init__(self):
        self.__config_utils = ConfigUtils()
    
    def count(self):
        """ 
        Count number of user accounts
        """
        config_data = self.__config_utils.get()
        
        
        # params = {"id":project_id,"user_id":config_data["user"]["id"]}        
        # headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        # result = requests.post(f'{config_data["api_endpoint"]}/users/stats', json=params, headers=headers)
        # stats = result.json()['results']
        # stats['data_values'] = stats['fields'] * stats['data_records']
        # print(f"Records counts: {stats['data_records']}")
        print("Not yet available.")
    
    def stats(self, username='', user_id=''):
        if not user_id and not username:
            print("A user name or user id is required.")
            return
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            return
        config_data = self.__config_utils.get()
        params = {"user_id":user_id}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/user/stats/u', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        print()

    def describe(self, username=''):        
        # if not username:
        #     print("user_id or username is required.")
        #     return
        # config_data = self.__config_utils.get()
        # params = {"search":username}       
        # headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        # result = requests.post(f'{config_data["api_endpoint"]}/profile/public', json=params, headers=headers)
        user = UserUtils().get_user(username)
        if user:
            print()
            print(json.dumps(user, indent=2, sort_keys=True))
        print()


class UserUtils(object):
    def __init__(self):
        self.__config_utils = ConfigUtils()

    def get_user(self, username):
        if not username:
            print("user_id or username is required.")
            return
        config_data = self.__config_utils.get()
        params = {"search":username}       
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/profile/public', json=params, headers=headers)
        user = {}
        if result:
            user = result.json()['results']
        if not user:
            print(f"User '{username}' not found.")
        return user