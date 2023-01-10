import os
# from https://github.com/Azure/azure-sdk-for-python/issues/26213
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import azure.ai.ml._artifacts._artifact_utilities as artifact_utils

subscription_id = "0b439d3d-c7ae-4a59-8b19-87226095eba0"
resource_group = "rg-mikou-dev"
workspace = "aml-mikou-dev"

dataset_name = "diabetes-dev-data"
dataset_version = "2"
downloaded_data_folder = "./data/"+dataset_name+"/"+dataset_version

# Get the client
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# Lookup the dataset to get the 'path'
data_info = ml_client.data.get(name=dataset_name, version=dataset_version)

# Download the dataset
artifact_utils.download_artifact_from_aml_uri(uri = data_info.path, destination = downloaded_data_folder, datastore_operation=ml_client.datastores)

# Verify it is downloaded
file_path = os.path.basename(data_info.path[10:])
assert os.path.exists(os.path.join(downloaded_data_folder, file_path))
