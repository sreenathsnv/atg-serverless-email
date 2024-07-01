from flask import Flask, request, jsonify
import boto3
import os
from werkzeug.datastructures import Headers
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

SES_CLIENT = boto3.client('ses', region_name='ap-south-1')  # Mumbai region

@app.route('/send', methods=['POST'])
def send_email():


    try:
        headers = Headers(request.headers)
    except KeyError as e:
        return jsonify({'message': 'Missing headers in request', 'error': str(e)}), 400


    data = request.get_json()

    try:
        email = validate_email(data['receiver_email']).email
    except EmailNotValidError as e:
        return jsonify({'message': str(e)}), 400

    
    try:
        response = SES_CLIENT.send_email(
        Source=os.getenv('EMAIL'),
        Destination={
            'ToAddresses': [email]
        },
        Message={
            'Subject': {
                'Data': data['subject']
            },
            'Body': {
                'Text': {
                    'Data': data['body_text']
                }
            }
        }
        )
        return jsonify({'message': 'Email sent successfully!', 'response': response})
    except Exception as e:
        return jsonify({'message': 'Failed to send email', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
