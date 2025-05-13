import shutil
import requests
import traceback
import os
from zipfile import ZipFile

def split_folder_to_zips(folder_path, zip_base_name, max_size=1 * 1024 * 1024 * 1024):
    """
    Split a folder into multiple zip files based on max size.

    Returns:
        list of zip file paths
    """
    zip_files = []
    current_size = 0
    part_number = 1
    current_zip_path = f"{zip_base_name}_part{part_number}.zip"
    current_zip = ZipFile(current_zip_path, 'w')

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not (file.lower().endswith('.jpg') or file.lower().endswith('.png')):
                continue

            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)

            if current_size + file_size > max_size:
                current_zip.close()
                zip_files.append(current_zip_path)

                # Start a new zip
                part_number += 1
                current_zip_path = f"{zip_base_name}_part{part_number}.zip"
                current_zip = ZipFile(current_zip_path, 'w')
                current_size = 0

            arcname = os.path.relpath(file_path, folder_path)
            current_zip.write(file_path, arcname)
            current_size += file_size

    current_zip.close()
    zip_files.append(current_zip_path)

    return zip_files


def upload_to_s3(base_url, zip_file,api_key, dataset_id):
    """
    Uploads a zip file containing images to the specified dataset on the server.

    Args:
        dataset_id (str): The ID of the dataset to which the images will be uploaded.
        zip_file_path (str): The local file path to the zip file containing the images.

    Returns:
        dict: The server's response as a dictionary, which may include details about the upload.

    Raises:
        Exception: If there is any issue with the network request or the server response.
    """
    try:
        print(f'Beginning Upload to S3 bucket')
        url = f"{base_url}/upload-dataset/"  # BASE_URL should be defined in the first cell of the notebook

        headers = {
            'Authorization': api_key,  # API_KEY should be defined in the second cell of the notebook
        }

        with open(zip_file, 'rb') as file:
            files = {'dataset_zip_file': file}
            data = {'dataset_id': dataset_id}  #cifar10

            response = requests.post(url, headers=headers, files=files, data=data)
            response.raise_for_status()

            print("Images uploaded successfully!")
            print(response.json())


    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        raise

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def main():
    try:
        print("Begin Main")
        base_url = "HOST_URL"
        api_key = "YOUR_API_KEY"

        src_path = "PATH_TO_DATASET"
        zip_file_path = "PATH_TO_DATASET_ZIP" #where you want to store the zip files - it will be deleted upon upload
        dataset_id = "YOUR_DATASET_ID" #dataset id

        print("Creating zip files...")
        zip_files = split_folder_to_zips(src_path, zip_file_path, max_size=1.8 * 1024 * 1024 * 1024)
        
        print("Uploading zip files...")
        for zip_file in zip_files:
            upload_to_s3(base_url, zip_file, api_key, dataset_id)
            os.remove(zip_file)

        print("All done!")

    except Exception as e:
        error_message = f"Error occurred in main: {e}\n{traceback.format_exc()}"
        print(error_message)

main()
