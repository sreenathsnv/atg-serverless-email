import json
import io
import sys
import base64
from werkzeug.wrappers import Response
from werkzeug.urls import url_parse
from werkzeug.datastructures import Headers
from app import app

def lambda_handler(event, context):
    body = event.get('body', '')
    if event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8')

    query_params = event.get('queryStringParameters') or {}
    query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])

    environ = {
        'wsgi.input': io.BytesIO(body.encode('utf-8')),
        'wsgi.errors': sys.stderr,
        'wsgi.version': (1, 0),
        'wsgi.run_once': True,
        'wsgi.url_scheme': 'https',
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': event.get('headers', {}).get('Content-Type', ''),
        'CONTENT_LENGTH': event.get('headers', {}).get('Content-Length', '0'),
        'SERVER_NAME': 'lambda',
        'SERVER_PORT': '80',
        'REMOTE_ADDR': event.get('requestContext', {}).get('identity', {}).get('sourceIp', '127.0.0.1'),
    }

    headers = Headers(event.get('headers', {}))
    for key, value in headers.items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

    response = Response()

    def start_response(status, response_headers, exc_info=None):
        response.status = status
        response.headers.extend(response_headers)
        return response.write

    result = app(environ, start_response)
    
    response.data = b''.join(result).decode('utf-8')
    response.content_length = len(response.data)

    return {
        'statusCode': int(response.status.split()[0]),
        'headers': {key: value for key, value in response.headers},
        'body': response.data
    }
