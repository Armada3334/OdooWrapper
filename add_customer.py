import xmlrpc.client
import ssl
from dotenv import load_dotenv
import os

def main(name, email, phone):

    load_dotenv()

    # Server configuration
    url = os.environ["URL"]
    db = os.environ["DB"]
    username = os.environ["USERNAME"]
    password = os.environ["API_KEY"]

    context = ssl._create_unverified_context()

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", context=context)


    # Auth
    uid = common.authenticate(db, username, password, {})
    if not uid:
        raise Exception("Authentication failed")
    print("Authenticated with UID:", uid)

    # Specify object endpoint
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", context=context)

    # Customer data
    customer_data = {
        'name': f"{name}",                       # Contact's name
        'email': f"{email}",                     # Email address
        'phone': f"{phone}",                     # Phone number
        'customer_rank': 1,                      # Typically indicates a customer
        'is_company': False,                     # False for an individual; True for a company
    }

    # Create the new customer contact record
    contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [customer_data])
    print("New customer contact created with ID:", contact_id)
    
if __name__ == "__main__":
    name = input("Enter name:")
    email = input("Enter email:")
    phone = input("Enter phone number:")

    main(name, email, phone)
