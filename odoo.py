from ml_customer import get_data
from add_customer import add_customer
import json
import os

directory = "./customer_forms"

#for filename in os.listdir(directory):
#    file_path = os.path.join(directory, filename)
#    if os.path.isfile(file_path):
#        data = get_data(file_path)
#        #print(data)
#        name = data['name']
#        email = data['email']
#        phone = data['phone']
#        street = data['street']
#        street2 = data['street2']
#        city = data['city']
#        state = data['state']
#        zip_code = data['zip_code']
#        vat = data['vat']
#        website = data['website']
#        mobile = data['mobile']
#        
#        #contact_id = add_customer(name=name, email=email, phone=phone, street=street, street2=street2, city=city, state=state, zip_code=zip_code, vat=vat, website=website, mobile=mobile)
#        
#        #print(f"Added customer with ID: {contact_id}")

data = [
    {
        "name": "PLUMBER WORKXS",
        "email": "JOHNW@LWORKXS.COM",
        "phone": "317 849 1212",
        "street": "5010 ST JOE HIGHWAY",
        "street2": None,
        "city": "CHELSEA",
        "state": "MI",
        "zip_code": "48118",
        "vat": None,
        "website": "WWW.LOMBERWORKKS.COM",
        "mobile": "787 4942"
    },
    {
        "name": "VINTAGE FURNISHINGS",
        "email": "VFURNISH@VF.COM",
        "phone": "(61) 555-1212",
        "street": "4998 ADAMS CENTER",
        "street2": None,
        "city": "CARSON",
        "state": "NV",
        "zip_code": "78182",
        "vat": None,
        "website": "WWW.VFURNISH.COM",
        "mobile": "2138476"
    },
    {
        "name": "MARTINDE DECOR",
        "email": "KTURNER@MARTIND.COM",
        "phone": "(374) 555-1212",
        "street": "7922 CENTER ST",
        "street2": None,
        "city": "LANSING",
        "state": "MI",
        "zip_code": "49204",
        "vat": "48947128",
        "website": "WWW.MARTINDECOR.COM",
        "mobile": None
    },
    {
        "name": "IF LAKESIDE FURNISHINGS",
        "email": "JOHN@LAKESIDEF.COM",
        "phone": "618 425 2748",
        "street": "802 NORTH ST",
        "street2": None,
        "city": "KENTWOOD",
        "state": "MN",
        "zip_code": "51189",
        "vat": None,
        "website": "WWW.LAKESIDEFURN.COM",
        "mobile": "618 475 2992"
    },
    {
        "name": "6006 HOME SUPPLY",
        "email": "CUSTSVC@COOLHEFTHOMES.COM",
        "phone": "(216) 425-1789",
        "street": "1347 MARTIN DR",
        "street2": None,
        "city": "NASHVILLE",
        "state": "IN",
        "zip_code": "37489",
        "vat": None,
        "website": "WWW.COOLHOMESTN.COM",
        "mobile": "12147986"
    },
    {
        "name": "BAKER HOME DESIGNS",
        "email": "BHOME@BAKERHDESIGNS.COM",
        "phone": "(218) 488 - 7123",
        "street": "6822 HICKORY LANE",
        "street2": None,
        "city": "WOODLAWN",
        "state": "IN",
        "zip_code": "46999",
        "vat": None,
        "website": "WWW.BAKERHOMEDESIGN.COM",
        "mobile": "8118214"
    },
    {
        "name": "STONEWALL HOMES",
        "email": "ROGER@STONEWALL.COM",
        "phone": "(274) 111-1212",
        "street": "128 NORTHSIDE DR.",
        "street2": None,
        "city": "LELAND",
        "state": "MI",
        "zip_code": "499",
        "vat": "67289714",
        "website": "WWW.STONEWALLHOMES.COM",
        "mobile": None
    },
    {
        "name": "GRAHAM FURNISHING",
        "email": "GRAHAMS@GFURNISH.COM",
        "phone": "(489) 416-1234",
        "street": "0217 E. WASHINGTON RD",
        "street2": None,
        "city": "MEMPHIS",
        "state": "TN",
        "zip_code": "50101",
        "vat": None,
        "website": "WWW.GRAHAMFURNISH.COM",
        "mobile": "9844672"
    },
    {
        "name": "MILLER DESIGNS",
        "email": "MILLER@MDESIGNS.COM",
        "phone": "(916) 462-1234",
        "street": "6782 MASON RD",
        "street2": None,
        "city": "MINTON",
        "state": "OH",
        "zip_code": "4618",
        "vat": None,
        "website": "WWW.MILLERDESIGNS.COM",
        "mobile": "2341562"
    },
    {
        "name": "TANNER LOMBERT DESIGNS",
        "email": "1.TANNERS@TLUMBER.COM",
        "phone": "(698) 421-1122",
        "street": "7270 CRESCENT AVE",
        "street2": None,
        "city": "FORT WAYNE",
        "state": "IN",
        "zip_code": "49824",
        "vat": "3542987",
        "website": "WWW.TANNERLUMBERDESIGNS.COM",
        "mobile": None
    }
]

for entry in data:
    name = entry['name']
    email = entry['email']
    phone = entry['phone']
    street = entry['street']
    street2 = entry['street2']
    city = entry['city']
    state = entry['state']
    zip_code = entry['zip_code']
    vat = entry['vat']
    website = entry['website']
    mobile = entry['mobile']
    
    contact_id = add_customer(
        name=name, email=email, phone=phone, street=street, 
        street2=street2, city=city, state=state, zip_code=zip_code, 
        vat=vat, website=website, mobile=mobile
    )
    print(f"Added customer with ID: {contact_id}")
