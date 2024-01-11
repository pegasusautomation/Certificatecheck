import json
from pymongo import MongoClient
# from urllib.request import ssl, socket
from datetime import datetime
import subprocess
port = 443

json_data = """
[
    {"servername": "Mediaroomserver01", "thumbprint":"0563B8630D62D75ABBC8AB1E4BDFB5A899B24D43"},
    {"servername": "Mediaroomserver02", "thumbprint":"A8985D3A65E5E5C4B2D7D66D40C6DD2FB19C5436"},
    {"servername": "Mediaroomserver03", "thumbprint":"CDD4EEAE6000AC7F40C3802C171E30148030C072"},
    {"servername": "Mediaroomserver04", "thumbprint":"A43489159A520F0D93D032CCAF37E7FE20A8B419"}
]
"""
# Convert JSON data to a Python object
data = json.loads(json_data)

try: 
    conn = MongoClient("mongodb+srv://garag9:zFg03iXmJcfHGvZS@cluster0.vn3o0wy.mongodb.net/?retryWrites=true&w=majority") 
    print("Connected To MongoDB successfully!!!") 
except:   
    print("Could not connect to MongoDB") 

# database 
db = conn.test

# Created or Switched to collection names: my_gfg_collection 
collection = db.certs 

def parse_cert_date(date_str):
    try:
        return datetime.strptime(date_str, "%A, %B %d, %Y %I:%M:%S %p")
    except ValueError:
        raise ValueError(f"Unable to parse date: {date_str}")
 
def get_certificate_expiration_days(thumbprint):
    powershell_cmd = f'Get-ChildItem Cert:\\LocalMachine\\root\\{thumbprint} | Select-Object -ExpandProperty NotAfter'
 
    res = subprocess.run(['powershell', '-Command', powershell_cmd], capture_output=True, text=True)
 
    exp_date_str = res.stdout.strip()
 
    exp_datetime = parse_cert_date(exp_date_str)
 
    rem_days = (exp_datetime - datetime.now()).days
 
    return rem_days

# Get total days left for expiry     
for item in data:
    daysToExpiration = get_certificate_expiration_days(item["thumbprint"])
    if daysToExpiration <= 30:
        status = "Expired"
    else:
        status = "Not Expired"

            # Code snippet to insert data to DB - Do not delete this block of code
    # emp_rec1 = { 
    #     "certname":item["servername"],
    #     "thumbprint":item["thumbprint"],  
    #     "noofdays":daysToExpiration, 
    #     "status":status
    #     }     
    # collection.insert_one(emp_rec1)

        # Code snippet to update records
    thumpprints = {"$set":{"thumbprint":item["thumbprint"]}}
    days = {"$set":{"noofdays":daysToExpiration}}
    certstatus = {"$set":{"status": status}}
    
    if item["servername"] == "Mediaroomserver01":
        myquery = {"servername":"Mediaroomserver01"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "Mediaroomserver02": 
        myquery = {"servername":"Mediaroomserver02"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "Mediaroomserver03": 
        myquery = {"servername":"Mediaroomserver03"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "Mediaroomserver04": 
        myquery = {"servername":"Mediaroomserver04"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
            
    print("Your certificate for" + " Server: %s" %(item["servername"]) + " will expire in : " + str(daysToExpiration) + " days")
            # if daysToExpiration == 34 or daysToExpiration == 1:
            #     send_notification(hostname,daysToExpiration,status)
            #     break