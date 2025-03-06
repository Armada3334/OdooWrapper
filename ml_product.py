from dotenv import load_dotenv
load_dotenv()

import os
import sys
import re
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

@def parse_product_ocr_text(ocr_text):
    

def get_product_data(image):
    image_path = image
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        print(f"Error reading file '{image_path}': {e}")
        sys.exit(1)
    
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'.")
        sys.exit(1)
    
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
    
    # Request OCR using the READ visual feature.
    visual_features = [VisualFeatures.READ]
    try:
        result = client.analyze(
            image_data=image_data,
            visual_features=visual_features,
            gender_neutral_caption=True,
            language="en"
        )
    except Exception as e:
        print("An error occurred during image analysis:")
        print(e)
        sys.exit(1)
    
    # Aggregate OCR text from detected blocks and lines.
    ocr_text = ""
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                ocr_text += line.text + "\n"
    else:
        print("No text detected in the image.")
        sys.exit(1)
    
    print(ocr_text)
    
    #extracted_data = parse_product_ocr_text(ocr_text)
    
    #return extracted_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python ml_product.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except Exception as e:
        print(f"Error reading file '{image_path}': {e}")
        sys.exit(1)
    
    try:
        endpoint = os.environ["VISION_ENDPOINT"]
        key = os.environ["VISION_KEY"]
    except KeyError:
        print("Missing environment variable 'VISION_ENDPOINT' or 'VISION_KEY'.")
        sys.exit(1)
    
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
    
    # Request OCR using the READ visual feature.
    visual_features = [VisualFeatures.READ]
    try:
        result = client.analyze(
            image_data=image_data,
            visual_features=visual_features,
            gender_neutral_caption=True,
            language="en"
        )
    except Exception as e:
        print("An error occurred during image analysis:")
        print(e)
        sys.exit(1)
    
    # Aggregate OCR text from detected blocks and lines.
    ocr_text = ""
    if result.read and result.read.blocks:
        for block in result.read.blocks:
            for line in block.lines:
                ocr_text += line.text + "\n"
    else:
        print("No text detected in the image.")
        sys.exit(1)
    
    print("OCR Text:")
    print(ocr_text)
    
    
    extracted_data = parse_customer_ocr_text(ocr_text)
    
    print("Extracted data:")
    print(extracted_data)

if __name__ == "__main__":
    main()
