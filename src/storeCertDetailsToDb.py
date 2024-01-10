from pymongo import MongoClient
import subprocess
from datetime import datetime
port = 443
servername = [""]
thumbprintlist = ["0563B8630D62D75ABBC8AB1E4BDFB5A899B24D43","A8985D3A65E5E5C4B2D7D66D40C6DD2FB19C5436"]
try: 
    conn = MongoClient("mongodb+srv://garag9:zFg03iXmJcfHGvZS@cluster0.vn3o0wy.mongodb.net/?retryWrites=true&w=majority") 
    print("Connected successfully!!!") 
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
for thumbprint in thumbprintlist:
    daysToExpiration = get_certificate_expiration_days(thumbprint)
    print(f"The certificate with thumbprint {thumbprint} expires in {daysToExpiration} days.")
    if daysToExpiration == 45:
        status = "Expired" 
    else:
        status = "Not Expired"
        # # Code snippet to insert data to DB
        # emp_rec1 = { 
        # "certname":thumbprint, 
        # "noofdays":daysToExpiration, 
        # "status":status
        # }     
        # collection.insert_one(emp_rec1)

        # Code snippet to update records

        days = {"$set":{"noofdays":daysToExpiration}}
        certstatus = {"$set":{"status": status}}
            
        if thumbprint == "0563B8630D62D75ABBC8AB1E4BDFB5A899B24D43":
            myquery = {"thumbprint":"0563B8630D62D75ABBC8AB1E4BDFB5A899B24D43"}
            collection.update_many(myquery.servername)                
            collection.update_many(myquery,days)
            collection.update_many(myquery,certstatus)
        elif thumbprint == "A8985D3A65E5E5C4B2D7D66D40C6DD2FB19C5436": 
            myquery = {"certname":"Mediaroomserver01"}
            collection.update_many(myquery,days)
            collection.update_many(myquery,certstatus)
        # elif hostname == "etsy.com": 
        #     myquery = {"certname":"etsy.com"}
        #     collection.update_many(myquery,days)
        #     collection.update_many(myquery,certstatus)
        # else: 
        #     myquery = {"certname":"nixcraft.com"}
        #     collection.update_many(myquery,days)
        #     collection.update_many(myquery,certstatus)
            
        print("Your certificate for" + " Server: %s" %(thumbprint) + " will expire in : " + str(daysToExpiration) + " days")
            # if daysToExpiration == 34 or daysToExpiration == 1:
            #     send_notification(hostname,daysToExpiration,status)
            #     break