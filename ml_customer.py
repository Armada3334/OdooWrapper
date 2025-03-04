from dotenv import load_dotenv
load_dotenv()

import os
import sys
import re
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def parse_ocr_text(ocr_text):
    """
    Parse OCR text from the image into a dictionary with keys:
    name, email, phone, street, street2, city, state, zip_code, vat, website, mobile.
    
    This parser uses heuristics based on a sample format.
    
    For example, given this OCR output:
    
      CUSTOMER DATA ENTRY FORM
      Individual @ Company
      LUMBER WORKXS
      Address
      5010 ST JOE HIGHWAY
      Phone
      317 849 1212
      CHELSEA
      Mi
      48118
      Mobile
      JOHNW@LWORKXS.COM
      Email
      787 4942
      Website
      WWW. LOMBERWORKKS.COM
      Tax ID ?
      ...
      
    It will assume:
      - Line 3 (index 2) is the customer name.
      - After "Address", the next line is the street.
      - After "Phone", the next line is the phone number, and then the following lines are:
            extra[0] → city,
            extra[1] → state,
            extra[2] → ZIP code.
      - Other labels such as "Mobile", "Email", and "Website" are handled accordingly.
      - The VAT value is determined by searching for any 7-digit numeric string within the OCR text.
    """
    # Split text into non-empty lines.
    lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
    data = {
        "name": None,
        "email": None,
        "phone": None,
        "street": None,
        "street2": None,
        "city": None,
        "state": None,
        "zip_code": None,
        "vat": None,
        "website": None,
        "mobile": None
    }
    n = len(lines)
    i = 0

    # Heuristic: if there are at least 3 lines, assume the third line is the customer name.
    if n >= 3:
        data["name"] = lines[2]

    # Define known labels (in lowercase).
    known_labels = {"address", "phone", "mobile", "email", "website"}
    
    while i < n:
        current = lines[i].lower()
        if current == "address":
            if i + 1 < n:
                data["street"] = lines[i+1]
                i += 2
                continue
        elif current == "phone":
            if i + 1 < n:
                data["phone"] = lines[i+1]
                i += 2
                # Collect extra details until the next known label.
                extra = []
                j = i
                while j < n and lines[j].lower() not in known_labels:
                    extra.append(lines[j])
                    j += 1
                if len(extra) >= 3:
                    data["city"] = extra[0]
                    data["state"] = extra[1]   # New field: state
                    data["zip_code"] = extra[2]
                    i = j
                continue
        elif current == "mobile":
            if i + 1 < n:
                value = lines[i+1]
                # If the value contains '@', assume it's an email (misplaced label).
                if "@" in value:
                    data["email"] = value
                else:
                    data["mobile"] = value
                i += 2
                continue
        elif current == "email":
            if i + 1 < n:
                value = lines[i+1]
                # If the value contains '@', assign as email.
                if "@" in value:
                    data["email"] = value
                else:
                    # Otherwise, if it looks like a long number, treat it as a mobile.
                    digits = re.sub(r"\D", "", value)
                    if len(digits) >= 10:
                        data["mobile"] = value
                    else:
                        data["email"] = value
                i += 2
                continue
        elif current == "website":
            if i + 1 < n:
                data["website"] = lines[i+1]
                i += 2
                continue
        elif current == "street2":
            if i + 1 < n:
                data["street2"] = lines[i+1]
                i += 2
                continue
        else:
            i += 1

    # After processing known labels, search for any 7-digit number (ignoring spaces)
    if data["vat"] is None:
        for line in lines:
            # Remove non-digit characters to form a candidate.
            candidate = re.sub(r"\D", "", line)
            if len(candidate) == 7:
                data["vat"] = candidate
                break

    return data

def get_data(image):
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
    
    extracted_data = parse_ocr_text(ocr_text)
    
    return extracted_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python ml_customer.py <path_to_image>")
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
    
    extracted_data = parse_ocr_text(ocr_text)
    
    print("Extracted data:")
    print(extracted_data)

if __name__ == "__main__":
    main()
