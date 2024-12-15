import os, time
from paddleocr import PaddleOCR
from pdf_img_convert import PDFtoImage
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from loguru import logger

class OCRProcessor:

    def __init__(self):
        self.pdf_img_convert = PDFtoImage()
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    def perform_ocr(self, file_path, output_folder):
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        images = self.pdf_img_convert.pdf_to_img_conversion(file_path,output_folder)
        if images:
            combined_text = ""
            for image in images:
                result = self.ocr.ocr(image, cls=True)
                for idx in range(len(result)):
                    res = result[idx]
                    for line in res:
                        text = line[1][0]
                        combined_text += f'{text} '
                combined_text += '\n'

        return str(combined_text.strip())