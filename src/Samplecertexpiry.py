from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

@app.route('/')

def get_certificate_expiry():
    try:
        xml_content = "C:\\Users\\Kothakota.Deepika_EX\\Certexpirysamplexml.xml"
        root = ET.parse(xml_content)
        timestamp_element = root.find(".//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Timestamp")
        expires_value = timestamp_element.find("{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Expires").text
        expires_datetime = datetime.strptime(expires_value, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_datetime = datetime.utcnow()
        remaining_days = (expires_datetime - current_datetime).days
        # Returning number of days to expiry
        return remaining_days
    except Exception as e:
        # return render_template(error=str(e)), 500
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
