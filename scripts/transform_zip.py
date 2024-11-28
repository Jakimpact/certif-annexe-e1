import os
import tarfile
import zipfile


# Variables 
zip_folder = os.getenv("zip_folder")
file_path = os.path.abspath(__file__)
dir_path = os.path.dirname(file_path).rsplit("/", 1)[0]
folder_path = dir_path + "/extracts/blobs/" + zip_folder


# Décompressage des fichiers zips
is_zip = True

while is_zip:
    is_zip = False

    for file in os.listdir(folder_path):

        if file.endswith(".zip"): 
            zip_path = os.path.join(folder_path, file)

            if zipfile.is_zipfile(zip_path):
                print("Fichier zip : ", file)
                with zipfile.ZipFile(zip_path, 'r') as zip_exp:
                    print("Contenu du fichier ZIP : ", zip_exp.namelist())
                    zip_exp.extractall(folder_path)
                os.remove(zip_path)
                is_zip = True
            else:
                print("Fichier zip invalide : ", file)

# Décompressage des fichiers tgz
is_tgz = True

while is_tgz:
    is_tgz = False

    for file in os.listdir(folder_path):

        if file.endswith(".tgz"): 
            tgz_path = os.path.join(folder_path, file)

            if tarfile.is_tarfile(tgz_path):
                print("Fichier tgz : ", file)
                with tarfile.open(tgz_path, 'r:gz') as tar_exp:
                    print("Contenu du fichier tgz : ", [member.name for member in tar_exp.getmembers()])
                    tar_exp.extractall(folder_path)
                os.remove(tgz_path)
                is_tgz = True
            else:
                print("Fichier tgz invalide : ", file)