import xmlrpc.client
import ssl
from dotenv import load_dotenv
import os

load_dotenv()

# Server configuration
url = os.environ["URL"]

context = ssl._create_unverified_context()
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/db", context=context)


# Get the list of databases
db_list = common.list()

print("Available Databases:", db_list)