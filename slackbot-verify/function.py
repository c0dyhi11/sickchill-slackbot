import json
from flask import request, Response
from flask import current_app


def main():
    request_body = json.loads(request.get_data())
    return Response(request_body['challenge'], status=200, mimetype='text/plain')

