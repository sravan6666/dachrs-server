import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import base64
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
local_path = os.getenv('FILE_LOCAL_PATH')
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


class BlobStorage(object):

    def uploadFile(epicUUID,fileName, fileBlob): 
        try:
            container_name = epicUUID
            blob_service_client.create_container(container_name)
            upload_file_path = os.path.join(local_path, fileName)
            dec = base64.b64decode(fileBlob)
            file = open(upload_file_path, 'wb')
            file.write(dec)
            file.close()
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=fileName)
            with open(upload_file_path, "rb") as data:
                response = blob_client.upload_blob(data)
            return {'status': True, 'message': 'File uploaded successfully', 'response': response}
        except Exception as ex:
            print('Exception:')
            print(ex)
            return {'status': False, 'message': 'Error File uploaded successfully', 'error': str(ex)}


    def downloadFile(epicUUID,fileName): 
        try:
            container_name = epicUUID
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=fileName)
            response = str(base64.b64encode(blob_client.download_blob().readall()))
            return {'status': True, 'blob': response}
        except Exception as ex:
            print('Exception:')
            print(ex)
            return {'status': False, 'message': 'Error File download - '+ str(ex)}