import os
import requests
from loguru import logger

class FileDownloader:
    def __init__(self):
        logger.info('FileDownloader initialised...')

    @staticmethod
    def download_file(file_link, folder_path):
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = os.path.basename(file_link)
        file_path = os.path.join(folder_path, file_name)

        try:
            response = requests.get(file_link, timeout=30)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                logger.success(f"File downloaded successfully: {file_path}")
                return file_path
            else:
                logger.info(f"Failed to download file: {response.status_code}")
                logger.info(f'Response: {response.text}')
        except requests.Timeout:
            logger.error(f"Request timed out after 30 seconds: {file_link}")
        except requests.RequestException as e:
            logger.error(f"Error downloading file: {str(e)}")
        
        return None
