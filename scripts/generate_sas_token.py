import os
from datetime import datetime, timedelta, timezone

from azure.storage.blob import (ContainerClient,
                                ContainerSasPermissions,
                                generate_container_sas)


# Variables 
account_key = os.getenv("account_key")
data_lake = os.getenv("data_lake")
blob_container = os.getenv("blob_container")


def create_service_sas_container(data_lake: str, blob_container: str, account_key: str):
    "Génération d'un token SAS pour un blob container avec une période de validité d'un jour"

    start_time = datetime.now(timezone.utc)
    expiry_time = start_time + timedelta(days=1)
    sas_token = generate_container_sas(
        account_name=data_lake,
        container_name=blob_container,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True, list=True),
        expiry=expiry_time,
        start=start_time
    )
    return sas_token


def create_container_client_sas():
    "Génération d'un container client avec le token sas pour accèder au container 'data'"

    sas_token = create_service_sas_container(data_lake, blob_container, account_key)
    sas_url = f"https://{data_lake}.blob.core.windows.net/{blob_container}?{sas_token}"
    container_client_sas = ContainerClient.from_container_url(sas_url)
    return container_client_sas
    
