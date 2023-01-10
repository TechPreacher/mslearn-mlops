# Import libraries

import os

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential

class DownloadADLS:
  def __init__(self, account_url, container_name):
    
    token_credential = DefaultAzureCredential()
    service_client = BlobServiceClient(
        account_url=account_url,
        credential=token_credential)
    
    self.client = service_client.get_container_client(container_name)

  def download(self, source, dest):
    '''
    Download a file or directory to a path on the local filesystem
    '''
    if not dest:
      raise Exception('A destination must be provided')

    blobs = self.ls_files(source, recursive=True)
    if blobs:
      # if source is a directory, dest must also be a directory
      if not source == '' and not source.endswith('/'):
        source += '/'
      if not dest.endswith('/'):
        dest += '/'
      # append the directory name from source to the destination
      dest += os.path.basename(os.path.normpath(source)) + '/'

      blobs = [source + blob for blob in blobs]
      for blob in blobs:
        blob_dest = dest + os.path.relpath(blob, source)
        self.download_file(blob, blob_dest)
    else:
      self.download_file(source, dest)

  def download_file(self, source, dest):
    '''
    Download a single file to a path on the local filesystem
    '''
    # dest is a directory if ending with '/' or '.', otherwise it's a file
    if dest.endswith('.'):
      dest += '/'
    blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

    print(f'Downloading {source} to {blob_dest}')
    os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
    bc = self.client.get_blob_client(blob=source)
    with open(blob_dest, 'wb') as file:
      data = bc.download_blob()
      file.write(data.readall())

  def ls_files(self, path, recursive=False):
    '''
    List files under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
      path += '/'

    blob_iter = self.client.list_blobs(name_starts_with=path)
    files = []
    for blob in blob_iter:
      relative_path = os.path.relpath(blob.name, path)
      if recursive or not '/' in relative_path:
        files.append(relative_path)
    return files

  def ls_dirs(self, path, recursive=False):
    '''
    List directories under a path, optionally recursively
    '''
    if not path == '' and not path.endswith('/'):
      path += '/'

    blob_iter = self.client.list_blobs(name_starts_with=path)
    dirs = []
    for blob in blob_iter:
      relative_dir = os.path.dirname(os.path.relpath(blob.name, path))
      if relative_dir and (recursive or not '/' in relative_dir) and not relative_dir in dirs:
        dirs.append(relative_dir)
    return dirs

# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # download data
    print("Starting Download...")

    client = DownloadADLS("dataspikestorage.blob.core.windows.net", "annotated")

    print("Downloading parquet file")
    client.download(source="2022/12/23/KA01LB1234/02ac5bd6-8cd6-4f9c-84fb-dadeac3b00a7/146618ee-9f8b-4d35-9d19-37c0c8dbf333", dest="/mnt/nfs/2022/12/23/KA01LB1234/02ac5bd6-8cd6-4f9c-84fb-dadeac3b00a7")

    #print("Downloading annotated data")
    #client.download(source="2022/12/23/KA01LB1234/02ac5bd6-8cd6-4f9c-84fb-dadeac3b00a7/146618ee-9f8b-4d35-9d19-37c0c8dbf111", dest="/mnt/nfs/2022/12/23/KA01LB1234/02ac5bd6-8cd6-4f9c-84fb-dadeac3b00a7")

    # add space in logs
    print("*" * 60)
    print("\n\n")
