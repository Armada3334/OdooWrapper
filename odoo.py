from ml_customer import get_data
from add_customer import add_customer
import json
import os

directory = "./customer_forms"

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        data = get_data(file_path)
        
        name = data['name']
        email = data['email']
        phone = data['phone']
        street = data['street']
        street2 = data['street2']
        city = data['city']
        state = data['state']
        zip_code = data['zip_code']
        vat = data['vat']
        website = data['website']
        mobile = data['mobile']
        
        contact_id = add_customer(name=name, email=email, phone=phone, street=street, street2=street2, city=city, state=state, zip_code=zip_code, vat=vat, website=website, mobile=mobile)
        
        print(f"Added customer with ID: {contact_id}")



