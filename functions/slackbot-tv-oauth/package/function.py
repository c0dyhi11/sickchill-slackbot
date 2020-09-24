import requests
import json
from helper import fetch_kube_data
from flask import request, Response
from flask import current_app


def get_token(url):
    headers = {'Accept': 'application/json'}
    rest_call = requests.post(url, headers=headers)
    return rest_call.text


def main():
    client_id = fetch_kube_data("secret", "default", "slackbot", "client-id")
    client_secret = fetch_kube_data("secret", "default", "slackbot", "client-secret")
    args = request.args
    code = args['code']
    oAuthURL = "https://slack.com/api/oauth.v2.access?client_id={}&client_secret={}&code={}".format(client_id, client_secret, code)
    access_token = get_token(oAuthURL)
    return access_token, 200

