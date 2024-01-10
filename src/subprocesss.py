import subprocess
from flask import Flask,Response,jsonify, request

app = Flask(__name__)
 
script_file = "C:/cert-react-app/createCert.ps1"

@app.route("/")
def createcert():
    try:
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_file], check=True, text=True, shell=True)
        print("PowerShell script executed successfully.")
        return {"alert" : 2}
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell script: {e}")

# @app.route('/api/query', methods = ['POST'])
# def get_query_from_react():
#     data = "Certificate created successfully"
#     try:
#         subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_file], check=True, text=True, shell=True)
#         print("PowerShell script executed successfully.")
#         return "Certificate created successfully"
#     except subprocess.CalledProcessError as e:
#         print(f"Error executing PowerShell script: {e}")
#     return "Hello"

if __name__ == "__main__":
    app.run(debug=True)