from loguru import logger
from pdf2image import convert_from_path
import os

class PDFtoImage():
     
    def __init__(self):
        logger.info('PDFtoImage class ready!')
        
    def pdf_to_img_conversion(self,file_path,outputFolderPath):
        try:  
            file_name = os.path.basename(file_path)
            images = convert_from_path(file_path,output_folder=outputFolderPath,fmt='jpg',thread_count=2,paths_only=True,output_file=file_name)
            total_images = len(images)
            logger.info(f'Total images after conversion: {total_images}')
            return images
        
        except Exception as e:
            logger.error(f'PDFtoImage pdfToImageConversion ERROR: {e}')
            return None