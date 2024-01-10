from urllib.request import ssl, socket
import datetime, smtplib
import pandas as pd
port = '587'

hostlist = ["google.com", "Yahoo.com", "etsy.com", "nixcraft.com","wmc.mr.tv3cloud.com"]
 

def send_notification(hostname,days_to_expire,status):
    smtp_port = 587
    smtpServer = "smtp.office365.com"
    receiverEmail = "raghavendra.ga9@outlook.com"
    "Raghavendra.Gandanahalli_EXT@medikind.com"
    "kothakota.deepika_ext@mediakind.com"
    senderEmail = "raghavendra.ga9@outlook.com"
    password = "Rathna@123"
    data = {
    'Name': hostname,
    'dates': days_to_expire,
    'status': status
    }
 
    df = pd.DataFrame(data)
 
 
    email_subject = "certificates status"
 
    html_table = df.to_html(index=False, classes='styled-table', escape=False)
 
    email_body = f"""
    <html>
    <head>
    <style>
    table {  border-collapse: collapse;         width: 100%;     }   
    th, td {  border: 1px solid #dddddd;         text-align: left;         padding: 8px;     }    
    th { background-color: #f2f2f2;     
    }
    </style>
    </head>
    <body>
    <p>Hello,</p>
    <p>Please find the certifcate status:</p>
        {html_table}
    </body>
    </html>
    """
 
    with smtplib.SMTP(senderEmail, smtp_port) as server:
        server.starttls()
        server.login(smtpServer, password)
    
        # Send the email with HTML and CSS styling
        server.sendmail(senderEmail, receiverEmail, f"Subject: {email_subject}\n\n{email_body}")

# # Send certificate expiry notification
# def send_notification(days_to_expire):
#     smtp_port = 587
#     smtp_server = "smtp.gmail.com"
#     sender_email = "devservicenow73@gmail.com"
#     receiver_email= "ga.rag9@gmail.com"
#     password = "uljmyygvkgdhlnmj"
#     if days_to_expire== 1:
#         days = "1 day"
#     else:
#         days = str(days_to_expire) + " days"
        
#     message = """\
#         Subject: Certificate Expiration
#         The TLS Certificate for your site expires in {days}"""
#     email_context = ssl.create_default_context()
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls(context = email_context)
#         server.login(sender_email, password)
#         server.sendmail(sender_email, 
#                         receiver_email, 
#                         message.format(days = days))

# Get total days left for expiry     
for hostname in hostlist:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname = hostname) as ssock:
            certificate = ssock.getpeercert()
            certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
            daysToExpiration = (certExpires - datetime.datetime.now()).days
            print("Your certificate for" + " Server: %s" %(hostname) + " will expire in : " + str(daysToExpiration) + " days")
            if daysToExpiration == 45 or daysToExpiration == 1:
                Status = "Expired"
            else: Status= "Not Expired"
            send_notification(hostname,daysToExpiration,Status)

# output : "{'subject': ((('commonName', '*.etsystatic.com'),),), 'issuer': ((('countryName', 'BE'),), (('organizationName', 'GlobalSign nv-sa'),), (('commonName', 'GlobalSign Atlas R3 DV TLS CA 2023 Q3'),)), 'version': 3, 'serialNumber': '01137C2C1B4AA69DEACCE9694079DB39', 'notBefore': 'Aug 23 10:46:56 2023 GMT', 'notAfter': 'Sep 23 10:46:55 2024 GMT', 'subjectAltName': (('DNS', '*.etsystatic.com'), ('DNS', 'api-origin.etsy.com'), ('DNS', 'api.etsy.com'), ('DNS', 'm.etsy.com'), ('DNS', 'openapi.etsy.com'), ('DNS', 'www.etsy.com'), ('DNS', 'etsy.com')), 'OCSP': ('http://ocsp.globalsign.com/ca/gsatlasr3dvtlsca2023q3',), 'caIssuers': ('http://secure.globalsign.com/cacert/gsatlasr3dvtlsca2023q3.crt',), 'crlDistributionPoints': ('http://crl.globalsign.com/ca/gsatlasr3dvtlsca2023q3.crl',)}"
