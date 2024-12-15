# Document Categorisation for Construction Products

## Problem Statement

**Parspec** is revolutionizing the sale of building construction products worldwide, digitizing and organizing the industry's product data, amounting to $5 trillion annually.

As part of enhancing product understanding, we seek to determine if a product document pertains to either of the 4 category classes.
- Lighting
- Fuses
- Cables
- Others

---

## [Demo](https://huggingface.co/spaces/HimankJ/SmartDocumentClassifier)

<img width="1219" alt="image" src="https://github.com/user-attachments/assets/6081e3ce-d274-4ee3-a95c-25fbfad48100" />

---

## Solution

To tackle the problem statement I have created a pipeline that will download the files using the URL, convert PDF to images, perform text extraction on these images i.e. OCR, and basis the text categorise the document into given 4 classes.

**Components:**

1. [DataLoader](classifier/src/data_loader.py)
- Handles downloading of files from URLs
- Added exception handling to log if url is invalid to failed to download file

2. [PDF to Image](classifier/src/pdf_img_convert.py)
- Here we convert input pdf to images
- We use `pdf2image` and `poppler` to convert pdf to images. The major advantage is that using poppler we can split pdf to images without losing any pixel data. The quality remains intact which is needed while performing text extraction

3. [Text Extraction](classifier/src/text_extractor.py)
- Here we perform OCR on images using [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR). 
- Currently PaddleOCR has not been optimised in terms of inference speed. As future scope we can finetune or add gpu components to reduce latency.

4. [Model Training](classifier/src/training.ipynb)
- Here we add our training and testing dataset to create final dataset
- Perform basic data understanding to understand class distribution
- Then we use train_test_split to create train (70%) and test (30%) dataset
- Then we build a scikit-learn pipeline using `TfidfTransformer` and `CountVectorizer`
- We train different models - SGD, Random Forest, SVC and Logistic Regression
- Also using accuracy and classification report we understand the performance of our models

## Questions & Answers

1. How long did it take to solve the problem?
- It took me about 3-4 hours to complete this entire problem statement. 

2. Explain your solution?
- The idea is to classify document basis text. After understanding the given data I felt text classification would be a good approach as it would capture the minute details that associates a document to a class. 

    Steps -
  
    2.1 Download data from input url
    
    2.2 Split pdfs to images
    
    2.3 Perform OCR for text extraction
    
    2.4 Model training and inference using input text
    
For more details refer [Solution](#solution) section above

3. Which model did you use and why?
- Dataset was used to train 4 models:
    - Random Forest
    - Stochastic Gradient Descent
    - Support Vector Classifier
    - Logistic Regression

Basis the performance all models seemed overfitted as accuracy is well above 99%. With my intuition and past experiences I decided to use Logistic Regression as it performs well on large unseen sample

4. Any shortcomings and how can we improve the performance?

There was various ways we can improve the performance/efficiency of current solution - 
- PDF to Image - Currently I have used poppler, as efficient as it is, it sometimes fails to convert pdf to images. In such scenarios we can have a fallback method to conver pdf to image

- Text Extraction - I have used PaddleOCR. It is one of the best open source model when it comes to text extraction. However it has its own bottleneck.

    - Inference speed - low response time on cpu devices, can be optimised using various in built parameters or by using gpu/fine-tuning
    - We can also opt to use paid ocr model likes AWS textract or Azure computer vision which are fast, accurate and cost effective

- Model training - Approach is text classification. It can work very well when trained on diverse and large samples. We can also add layout features such as table count, headers, sub headers etc.

5. Report the model's performance on the test data using an appropriate
metric. Explain why you chose this particular metric.

The metric I have choosen is Accuracy, Precision and Recall.

Accuracy for all models - 
- Random Forest: 99.7%
- **Logistic Regression: 99.5%**
- SVC: 99.2%
- SGD: 99.5%

Final model - Logistic Regression
Although the accuracy is almost same for all models, I have choosen Logistic regression as final model. 

Accuracy is a good evaluation metric when it comes to classification tasks. Along with that Precision and recall are also helpful in understanding false positive rate. However in given situation all these metrics are close due to less diverse data and limited samples.

---
