import gradio as gr
import os, pickle
from text_extractor import OCRProcessor
import shutil
from loguru import logger

class DocumentClassifier:
    def __init__(self):
        self.ocr_processor = OCRProcessor()
        with open('model/lr_classifier_v1.pkl', 'rb') as doc_cat_file:
            self.model = pickle.load(doc_cat_file)
        
        # Create temporary directories
        self.temp_folder = 'temp_files'
        self.temp_output = 'temp_output'
        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.temp_output, exist_ok=True)
        self.label_mapper = {
            0: 'cable',
            1: 'fuses',
            2: 'lighting',
            3: 'others'
        }

    def cleanup(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_folder, ignore_errors=True)
        shutil.rmtree(self.temp_output, ignore_errors=True)

    def process_document(self, file):
        try:
            file_path = file.name
            # Perform OCR
            raw_text = self.ocr_processor.perform_ocr(
                file_path, 
                self.temp_output
            )
            
            if not raw_text:
                return "No text could be extracted from the document"

            predicted_probabilities = self.model.predict_proba([raw_text])[0]
            predicted_category_index = predicted_probabilities.argmax()
            predicted_category = self.label_mapper[predicted_category_index]
            confidence_score = predicted_probabilities[predicted_category_index]
            
            self.cleanup()
            
            return {
                'Classification': predicted_category,
                'Confidence Score': str(round(confidence_score, 2))
            }

        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            self.cleanup()
            return f"Error processing document: {str(e)}"

classifier = DocumentClassifier()

def classify_document(file):
    result = classifier.process_document(file)
    return result['Classification'], result['Confidence Score']

iface = gr.Interface(
    fn=classify_document,
    inputs=gr.File(label="Upload PDF or Image"),
    outputs=[
        gr.Label(label="Classification"),
        gr.Label(label="Confidence Score")
    ],
    title="📄 Smart Document Classifier",
    description="Upload your PDF or image documents and let AI classify them automatically into categories: cable, fuses, lighting, or others.",
    theme=gr.themes.Citrus(), 
    css="""
        .gradio-container {
            font-family: 'Quicksand', sans-serif !important;
        }
        .gr-button {
            font-weight: 600;
        }
    """
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
