import os
import json
#main.py

def app(wsgi_environ, start_response):
    data = dict(branch=os.environ.get('APP_BRANCH', 'unknown'),
                commit=os.environ.get('APP_COMMIT', 'unknown'))

    data_as_json = json.dumps(data)
    data_as_bytes = bytes(data_as_json, 'utf-8')

    status = '200 OK'
    response_headers = [
        ('Content-type', 'application/json'),
        ('Content-Length', str(len(data_as_bytes)))
    ]

    print(f'returning: {data_as_json}')
    start_response(status, response_headers)
    return iter([data_as_bytes])
