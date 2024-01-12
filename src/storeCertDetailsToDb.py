import json
from pymongo import MongoClient
# from urllib.request import ssl, socket
from datetime import datetime
import subprocess
port = 443
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
serverName_list = []
thumbPrint_list = []
noOfdays_list = []
certStatus_list = []

json_data = """
[
    {"servername": "MEDIAROOM_SERVER_01", "thumbprint":"0563B8630D62D75ABBC8AB1E4BDFB5A899B24D43"},
    {"servername": "MEDIAROOM_SERVER_02", "thumbprint":"A8985D3A65E5E5C4B2D7D66D40C6DD2FB19C5436"},
    {"servername": "MEDIAROOM_SERVER_03", "thumbprint":"CDD4EEAE6000AC7F40C3802C171E30148030C072"},
    {"servername": "MEDIAROOM_SERVER_04", "thumbprint":"A43489159A520F0D93D032CCAF37E7FE20A8B419"}
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
    serverName_list.append(item["servername"])
    thumbPrint_list.append(item["thumbprint"])
    noOfdays_list.append(daysToExpiration)
    certStatus_list.append(status)
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
    
    if item["servername"] == "MEDIAROOM_SERVER_01":
        myquery = {"servername":"MEDIAROOM_SERVER_01"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "MEDIAROOM_SERVER_02": 
        myquery = {"servername":"MEDIAROOM_SERVER_02"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "MEDIAROOM_SERVER_03": 
        myquery = {"servername":"MEDIAROOM_SERVER_03"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
    elif item["servername"] == "MEDIAROOM_SERVER_04": 
        myquery = {"servername":"MEDIAROOM_SERVER_04"}
        collection.update_many(myquery,thumpprints)                
        collection.update_many(myquery,days)
        collection.update_many(myquery,certstatus)
            
    print("Your certificate for" + " Server: %s" %(item["servername"]) + " will expire in : " + str(daysToExpiration) + " days")
            # if daysToExpiration == 34 or daysToExpiration == 1:
            #     send_notification(hostname,daysToExpiration,status)
            #     break
# Create a DataFrame
data1 = {'Server Name': serverName_list,
    'Thumb Print': thumbPrint_list,
    'Days to Expire': noOfdays_list,
    'Status': certStatus_list}
df = pd.DataFrame(data1)

html_style = df.to_html(index=False,bold_rows=True)
styled_html_table = f""" <html><head><style ="padding:20px;"margin:20px;">table{{font-family: Arial,font-size:5vw;sans-serif;cellspacing=0;border-collapse: collapse;width: 10%;border: 1px solid #000000;}}th,td{{border: 1px solid #dddddd;   text-align: left;}}th {{ background-color: #f2f2f2;width:1%;}} td{{width: 1%;white-space:nowrap;}} tr{{ padding: 0;}}</style> </head> <body>{html_style}</body> </html> """
# Set up your email credentials and message
sender_email = 'raghavendra.ga9@outlook.com'
sender_password = 'Rathna@123'
receiver_email = 'raghavendra.ga9@outlook.com'

subject = 'Certificate Status Alert'
body = f'<br><b style ="color:red;">CERTIFICATE STATUS :</b><br><br>{styled_html_table}'

# Create MIME object
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

# Attach the HTML table to the email body
message.attach(MIMEText(body, 'html'))

# Connect to SMTP server and send the email
with smtplib.SMTP('smtp.office365.com', 587) as server:
    server.starttls()
    server.login(sender_email, sender_password)

# Send email
    server.sendmail(sender_email, receiver_email, message.as_string())
