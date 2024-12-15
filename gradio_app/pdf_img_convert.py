from loguru import logger
from pdf2image import convert_from_path
import os, shutil

class PDFtoImage():
     
    def __init__(self):
        logger.info('PDFtoImage class ready!')
        
    def pdf_to_img_conversion(self,file_path,outputFolderPath):
        if not os.path.exists(outputFolderPath):
            os.makedirs(outputFolderPath)
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == '.pdf':
                file_name = os.path.basename(file_path)
                images = convert_from_path(file_path,output_folder=outputFolderPath,fmt='jpg',thread_count=2,paths_only=True,output_file=file_name)
                total_images = len(images)
                logger.info(f'Total images after conversion: {total_images}')
                return images
            else:
                logger.info(f'Input type is not PDF, no conversion needed')
                file_name = os.path.basename(file_path)
                image_path = os.path.join(outputFolderPath, file_name)
                shutil.copy2(file_path, image_path)
                return [image_path]
        
        except Exception as e:
            logger.error(f'PDFtoImage pdfToImageConversion ERROR: {e}')
            return None