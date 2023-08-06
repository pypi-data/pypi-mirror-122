import os
import requests
import json
import tabulate
import pandas as pd
from colorama import Fore, Style
from opinecli.config import ConfigUtils
from opinecli.user import UserUtils

class Project(object):
    def __init__(self):
        self.__config_utils = ConfigUtils() 
    
    def list(self, username='', user_id='', org='o', output='table'):
        config_data = self.__config_utils.get()
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        params = {"user_id": user_id,"org_id":org,"private":"1"}
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/projects/user', json=params, headers=headers)
        keys = ['id','title','owner_id', 'created', 'modified']
        print()

        if not result.json()['results']:
            print("No data available.")
            return

        if output == 'json':
            data = [{key: item[key] for key in keys} for item in result.json()['results']] 
            print(json.dumps(data, indent=2))
        elif output == 'table':
            df = pd.DataFrame(result.json()['results'])
            df = df[keys]
            print(tabulate.tabulate(df, headers=keys, tablefmt="simple", colalign=("left",)))
        print()

    def describe(self, project_id='', username='', user_id='', detail=0):
        config_data = self.__config_utils.get()
        if not project_id:
            project_id = ProjectUtils().get_default_project()
        if not project_id:
            return ""
        if username:
            print(username)
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        params = {"project_id":project_id, "user_id":user_id, "detailed": str(detail)}        
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/projects', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['results'], indent=2, sort_keys=True))
        print()

    def stats(self, project_id='', username='', user_id='', output='table'):
        """ 
        Get project statistics
        """
        config_data = self.__config_utils.get()
        if not project_id:
            project_id = ProjectUtils().get_default_project()
        if not project_id:
            return ""
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        params = {"project_id":project_id,"user_id":user_id}        
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/projects/stats', json=params, headers=headers)
        stats = result.json()['results']
        stats['data_values'] = stats['fields'] * stats['data_records']
        print()

        if not result.json()['results']:
            print("No data available.")
            return
            
        if output == 'json':
            print(json.dumps(stats, indent=2))
        elif output == 'table':
            print(tabulate.tabulate([(k, v) for k,v in stats.items()]))
        print()

    def lock(self, project_id='', username='', user_id=''):
        config_data = self.__config_utils.get()
        if not project_id:
            project_id = ProjectUtils().get_default_project()
        if not project_id:
            return "Project id is required"
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        
        params = {"project_id":project_id,"owner_id":config_data["user"]["id"], "locked":1}        
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/projects/lock', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['message']['message']))
        print()

    def unlock(self, project_id='', username='', user_id=''):
        config_data = self.__config_utils.get()
        if not project_id:
            project_id = ProjectUtils().get_default_project()
        if not project_id:
            return "Project id is required"
        if username:
            user = UserUtils().get_user(username)
            if user:
                user_id  = user['id']
        if not user_id:
            user_id = config_data["user"]["id"]
        
        params = {"project_id":project_id,"owner_id":config_data["user"]["id"], "locked":0}        
        headers = {"content-type": "application/json", "authorization": f'Token {config_data["user"]["access_token"]}'}        
        result = requests.post(f'{config_data["api_endpoint"]}/projects/lock', json=params, headers=headers)
        print()
        print(json.dumps(result.json()['message']['message']))
        print()

class ProjectUtils(object):

    def __init__(self):
        self.__config_utils = ConfigUtils() 

    def get_default_project(self):
        config_data = self.__config_utils.get()
        if 'project_id' not in config_data:
            print()
            print(Fore.RED + 'A project id is required. See --help' + Style.RESET_ALL)
            print()
            return
        else:
            project_id = config_data['project_id']
            print()
            print(Style.BRIGHT + Fore.CYAN + "project_id: " + project_id + Style.RESET_ALL)
            return project_id