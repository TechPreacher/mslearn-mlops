import os, uuid, sys
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from azure.identity import ClientSecretCredential
from azure.identity import DefaultAzureCredential

def initialize_storage_account_ad(storage_account_name):
    
    try:  
        global service_client

        credential = DefaultAzureCredential()

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=credential)

        print(service_client);
    
    except Exception as e:
        print(e)

initialize_storage_account_ad("dataspikestorage")