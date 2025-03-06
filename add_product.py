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

def add_product():
    print("funny")

if __name__ == "__main__":
    # Prompt user for customer details
    print("Enter new product details:")
    

    add_product()
