import requests
import json
import tabulate
import pandas as pd
from opinecli.config import ConfigUtils
from opinecli.user import UserUtils

class Subscription(object):
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
    
    def stats(self):
        """ Get counts of various subscription types"""
        print("Not yet available.")

    def describe(self, username, user_id=''):   
        config_data = self.__config_utils.get()
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]     
        if not user_id:
            print("user_id is required.")
            return
        
        params = {"user_id":user_id}       
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/profile/subscription', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        print()

    def pay(self, username, user_id='', type='full'):
        """Confirm payment of user's subscription. Payment type can be 'full' or 'partial'"""
        config_data = self.__config_utils.get()
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            print("user_id is required.")
            return
        
        params = {"user_id":user_id, "full_payment": type}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/payment/add', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        print()

    def payments(self, username, user_id='',output='table'):
        """ Get a list of payments made by a user"""
        config_data = self.__config_utils.get()
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        params = {"user_id": user_id}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/subscription/payments', json=params, headers=headers)
        keys = ['subs_id','cycle_paid_for','full_payment', 'date_paid', 'reference_no', 'created']
        print()
        if output == 'json':
            data = [{key: item[key] for key in keys} for item in result.json()['results']] 
            print(json.dumps(data, indent=2))
        elif output == 'table':
            df = pd.DataFrame(result.json()['results'])
            df.sort_values(by=['created'])
            df = df[keys]
            print(tabulate.tabulate(df, headers=keys, tablefmt="simple", colalign=("left",)))
        print()