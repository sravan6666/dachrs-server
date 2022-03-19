from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from os import environ as env

keyVaultName = env["KEY_VAULT_NAME"]
print(keyVaultName)
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

class SecretManager(object):
    def get_secret_value(secret_name):
        retrieved_secret = client.get_secret(secret_name, logging_enable=True)
        print(f"Your secret is '{retrieved_secret.value}'.")
        return retrieved_secret.value