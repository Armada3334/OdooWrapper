import xmlrpc.client
import ssl
import os
from dotenv import load_dotenv

# Load environment variables once at the start
load_dotenv()
URL = os.environ.get("URL")
DB = os.environ.get("DB")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("API_KEY")

def get_xmlrpc_proxies(url, context):
    """Create XML-RPC proxies for common and object endpoints."""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", context=context)
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", context=context)
    return common, models

def authenticate(common, db, username, password):
    """Authenticate and return the user ID (uid)."""
    uid = common.authenticate(db, username, password, {})
    if not uid:
        raise Exception("Authentication failed")
    print("Authenticated with UID:", uid)
    return uid

def add_customer(name, email, phone, street=None, street2=None, city=None, zip_code=None,
                 state=None, vat=None, website=None, mobile=None):
    """
    Create a new customer contact in Odoo with extended details.
    
    Parameters:
        name (str): Customer's name.
        email (str): Customer's email.
        phone (str): Customer's primary phone.
        street (str, optional): Street address.
        street2 (str, optional): Secondary street address.
        city (str, optional): City.
        zip_code (str, optional): Postal/ZIP code.
        state (str, optional): State name or abbreviation (will be looked up in the US states).
        vat (str, optional): Tax ID (VAT number).
        website (str, optional): Website URL.
        mobile (str, optional): Mobile phone number.
    
    Returns:
        int: The new customer record ID.
    """
    # Create an SSL context that bypasses certificate verification
    context = ssl._create_unverified_context()

    common, models = get_xmlrpc_proxies(URL, context)
    uid = authenticate(common, DB, USERNAME, PASSWORD)

    # Build the customer data dictionary
    customer_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'customer_rank': 1,     # Indicates a customer
        'is_company': True,    # False for an individual
    }
    if street:
        customer_data['street'] = street
    if street2:
        customer_data['street2'] = street2
    if city:
        customer_data['city'] = city
    if zip_code:
        customer_data['zip'] = zip_code
    if vat:
        customer_data['vat'] = vat
    if website:
        customer_data['website'] = website
    if mobile:
        customer_data['mobile'] = mobile

    # Set the country to United States (always)
    us_country_ids = models.execute_kw(DB, uid, PASSWORD, 'res.country', 'search', [[['name', '=', 'United States']]])
    if us_country_ids:
        customer_data['country_id'] = us_country_ids[0]
    else:
        raise Exception("United States not found in country records.")

    # If state is provided, search for it by full name or code and add it to the customer data
    if state:
        # Search for state where name equals state OR code equals uppercase version of state
        state_ids = models.execute_kw(
            DB, uid, PASSWORD, 'res.country.state', 'search',
            [[('country_id', '=', us_country_ids[0]), '|', ('name', '=', state), ('code', '=', state.upper())]]
        )
        if state_ids:
            customer_data['state_id'] = state_ids[0]
        else:
            print(f"State '{state}' not found for United States. Skipping state assignment.")

    # Create the customer record in Odoo
    contact_id = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'create', [customer_data])
    print("New customer contact created with ID:", contact_id)
    return contact_id

if __name__ == "__main__":
    # Prompt user for customer details
    print("Enter new customer details:")
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    street = input("Street (optional): ") or None
    street2 = input("Street2 (optional): ") or None
    city = input("City (optional): ") or None
    zip_code = input("ZIP Code (optional): ") or None
    state = input("State (optional): ") or None
    vat = input("Tax ID (VAT, optional): ") or None
    website = input("Website (optional): ") or None
    mobile = input("Mobile (optional): ") or None

    add_customer(name, email, phone, street, street2, city, zip_code, state, vat, website, mobile)
