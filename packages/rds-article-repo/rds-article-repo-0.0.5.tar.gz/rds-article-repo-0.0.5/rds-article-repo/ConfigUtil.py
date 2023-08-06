import boto3, json
import secrets
import re
import os
import requests

class GlobalConfig:
    def __init__(self, bucketName:str, objectPath: str):
        self.bucketName = bucketName
        self.objectPath = objectPath
        s3_resource = boto3.resource('s3')
        
        s3_object=s3_resource.Bucket(bucketName).Object(key=objectPath).get()['Body']
        self.configMap = json.load(s3_object)

    def getDBConfigurations(self, dbName):
        for db in self.configMap['dbConfigurations']:
            if db['dbName']==dbName:
                return self._resolveSecrets(db)

        return self.configMap['dbConfigurations']

    def getSmtpDetails(self):
         return self._resolveSecrets(self.configMap['smtpDetails'])

    def getGeneralProperties(self, key=None):
        for entry in self.configMap['generalProperties']:
            if entry['key']==key:
                return entry
                
        return self.configMap['generalProperties']

    def getAll(self):
        return self.configMap
    
    #it only a dict object
    #TODO for list json
    def _resolveSecrets(self, config):
        for key, val in config.items():
            if isinstance(val, str) and "rsm:" in val:
                secretVal = getSecret(re.sub('[${}]',"",  val.replace("rsm:","")))
                config[key] = secretVal
        return config

def getEnv():
    return os.environ.get("aws_env")


def getSecret(secretKey=''):
    vault_base_url = os.environ['SPR_APP_SECRET_HC_VAULT_BASE_URL']
    vault_token = os.environ['SPR_APP_SECRET_HC_VAULT_TOKEN']
    vault_shelf_id = os.environ['IDF_SHELF_ID']
    
    url = vault_base_url + "/" + vault_shelf_id
    
    headers = {"spr-sm-token": vault_token}
    params = {"secret-keys" : secretKey}
    
    resp = requests.get(url = url, params = params, headers=headers)
    
    return resp.json()['data']