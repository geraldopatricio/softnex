import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


class Cofre:

    def __init__(self):
        keyVaultName = os.getenv("KEY_VAULT_NAME")
        KVUri = "https://" + keyVaultName + ".vault.azure.net"
        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=KVUri, credential=credential)

    def get_secret_azure(self, secret):
        return self.client.get_secret(secret).value
