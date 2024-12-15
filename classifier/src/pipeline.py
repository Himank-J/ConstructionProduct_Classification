import pandas as pd
from data_loader import FileDownloader
from text_extractor import OCRProcessor
import os, shutil, time
from loguru import logger
import os
import pandas as pd

class Pipeline:

    def __init__(self, excel_file, folder_path, output_folder_path):
        self.excel_file = excel_file
        self.folder_path = folder_path
        self.output_folder_path = output_folder_path
        self.ocr_processor = OCRProcessor()

    def load_and_download(self, sheet_name):

        df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
        logger.info(f'Shape: {df.shape}')

        for index, row in df.iterrows():
            file_link = row['datasheet_link'] 
            try:
                file_path = FileDownloader.download_file(file_link, self.folder_path)
                if file_path:
                    raw_text, page_count = self.ocr_processor.perform_ocr(file_path, self.output_folder_path)
                    df.at[index,'raw_text'] = raw_text
                    df.at[index,'page_count'] = page_count

                logger.info(f'Processed file {index+1}')
                shutil.rmtree(self.folder_path, ignore_errors=True)
                shutil.rmtree(self.output_folder_path, ignore_errors=True)
                logger.info('-----------------------')
                
                if index % 100 == 0 and index != 0:
                    df.to_csv('DataSet_postocr_test.csv',index=False)
                    time.sleep(2)
                    # break
            except Exception as e:
                logger.error(e)

        df.to_csv('DataSet_postocr_test.csv',index=False)

data_path = os.path.abspath('data/DataSet.xlsx')
file_dirs = 'class_data'
output_dir = 'img_data'
pipeline = Pipeline(data_path, file_dirs, output_dir)

sheet_name = 'test_data'
pipeline.load_and_download(sheet_name=sheet_name)