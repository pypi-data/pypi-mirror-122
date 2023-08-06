import requests 
from requests.auth import HTTPBasicAuth 
import json
from dotenv import dotenv_values
env_settings = dotenv_values(".env")


class Dataset():       
    # Dataset Class
    # 
    # Methods:
    # read_all()
    # read_by_id(dataset_id)
    # read_by_name(dataset_name, repo_id=None)
    # 
    

    def __init__(self, api_key):
        self.api_key = api_key

    def read_all(self):    
        url = "http://api.alphacast.io/datasets"
        r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
        return json.loads(r.content)

    def read_by_id(self, dataset_id):
            url = "http://api.alphacast.io/datasets/{}".format(dataset_id)
            r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
            return json.loads(r.content)

    def read_by_name(self, dataset_name, repo_id= None):
        url = "http://api.alphacast.io/datasets"
        
        r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
        dataset = None
        for element in json.loads(r.content):
            if (element["name"] == dataset_name) & ((element["repositoryId"] == repo_id) | (repo_id== None)):
                return element
            #print(element)
        return dataset

class Repository():   
    # Repository Class
    # 
    # Methods:
    # read_all()
    # read_by_id(dataset_id)
    # read_by_name(dataset_name, repo_id=None)
    # create(repo_name, repo_description=None, privacy="Private", slug=None, returnIdIfExists=False)

    def __init__(self, api_key):
        self.api_key = api_key

    def read_all(self):
        url = "http://api.alphacast.io/repositories"
        r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
        return json.loads(r.content)

    def read_by_id(self, repository_id):
            url = "http://api.alphacast.io/repositories/{}".format(repository_id)
            r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
            return json.loads(r.content)

    def read_by_name(self, repo_name):
        url = "http://api.alphacast.io/repositories"
        r = requests.get(url, auth=HTTPBasicAuth(self.api_key, ""))
        repos = json.loads(r.content)
        for element in repos:
            if (element["name"] == repo_name):
                return element
        return False

    def create(self, repo_name, repo_description=None, privacy="Private", slug=None, returnIdIfExists=False):
        if not slug:
            slug = repo_name.lower().replace(" ", "-")
        if not repo_description:
            repo_description = repo_name
        
        exists = self.read_by_name(repo_name)
        if exists:
            if returnIdIfExists:
                return exists
            else:
                raise ValueError("Repository already exists: {}".format(exists["id"]))

        url = "http://api.alphacast.io/repositories"
        
        form={
            "name": repo_name,
            "description": repo_description,
            "privacy": privacy,
            "slug": slug    
        }

        return json.loads(requests.post(url, data=form, auth=HTTPBasicAuth(self.api_key, "")).content)

class Session():   
    # Session Class(api_key)
    # 
    # Methods:
    # repository
    # dataset

    def __init__(self, api_key):
        self.api_key = api_key
        self.repository = Repository(self.api_key) 
        self.dataset = Dataset(self.api_key)    
        



    

# Instantiate a Multiplication object
#session = Session("ak_IljfMJiTQJb89bPy6MQx")

# Call the multiply method
#print(session.repositories)