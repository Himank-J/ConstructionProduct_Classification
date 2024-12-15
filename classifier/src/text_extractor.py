import os, time
from paddleocr import PaddleOCR
from pdf_img_convert import PDFtoImage
from loguru import logger

class OCRProcessor:

    def __init__(self):
        self.pdf_img_convert = PDFtoImage()
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
    def getText(self,file_path):

        page_count = 0
        raw_text = ''
        try:
            read_response = None

            with open(os.path.abspath(f'{file_path}'), 'rb') as image:
                read_response = self.__cvClient.read_in_stream(image, raw=True)

            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            while True:
                read_result = self.__cvClient.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(0.2)
        
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        raw_text += line.text + '\n'
                    page_count += 1

        except Exception as e:
            logger.info(str(e))
            logger.info('Error file name:'+ str(file_path))

        return raw_text, page_count
    
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
                        # print('line',line)
                        # print('line',line[1][0])
                        text = line[1][0]
                        combined_text += f'{text} '
                    # break
                combined_text += '\n'

        return combined_text.strip()
