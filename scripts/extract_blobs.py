import os

from generate_sas_token import create_container_client_sas


# Variables 
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path).rsplit("/", 1)[0]
extract_path = dir_path + "/extracts/blobs"
folders = [
    os.getenv("parquet_folder"),
    os.getenv("csv_folder"),
    os.getenv("zip_folder")
    ]
container_client_sas = create_container_client_sas()


class Extractor:
    def __init__(self, container_client, folder_name):
        self.parent_folder_name = folder_name
        self.container_client = container_client

    def create_folder(self, folder_path):
        folder_path = extract_path + "/" + folder_path
        os.makedirs(folder_path, exist_ok=True)

    def get_blobs(self):
        """
            Récupération des blobs du folder contenu dans le container data.
            Itération sur les blobs et identification des dossiers / fichiers
            pour lancer la méthode adéquate.
        """

        blobs = self.container_client.list_blobs(name_starts_with=self.parent_folder_name)

        file = False
        for blob in blobs:
            if "." not in blob.name:
                self.create_folder(blob.name)

            else:
                self.download_blob(blob)
                file = True

    def download_blob(self, blob):
        """Téléchargement du fichier blob"""

        blob_parquet = self.container_client.get_blob_client(blob)
        blob_name_chunks = blob.name.rsplit("/", 1)
        with open(f"{extract_path}/{blob_name_chunks[0]}/{blob_name_chunks[1]}", "wb") as dl_file:
            dl_file.write(blob_parquet.download_blob().readall())
            print(f"Fichier téléchargé : extracts/blobs/{blob_name_chunks[0]}/{blob_name_chunks[1]}")


if __name__ == "__main__":
    
    for folder in folders:
        folder_extractor = Extractor(container_client_sas, folder)
        folder_extractor.get_blobs()