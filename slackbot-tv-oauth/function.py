import requests
import json
from flask import request, Response
from flask import current_app


def get_token(url):
    headers = {'Accept': 'application/json'}
    rest_call = requests.post(url, headers=headers)
    return rest_call.text


def fetch_kube_data(data_type, namespace, secret_name, secret_key):
    if data_type.lower() == "secret":
        data_type = "secrets"
    elif data_type.lower() == "configmap":
        data_type = "configs"
    elif data_type.lower() == "config":
        data_type = "configs"
    else:
        data_type = data_type.lower()
    path = "/{}/{}/{}/{}".format(data_type, namespace, secret_name, secret_key)
    f = open(path, "r")
    kube_data = f.read()
    f.close()
    return kube_data


def main():
    client_id = fetch_kube_data("secret", "default", "slackbot", "client-id")
    client_secret = fetch_kube_data("secret", "default", "slackbot", "client-secret")
    args = request.args
    code = args['code']
    oAuthURL = "https://slack.com/api/oauth.v2.access?client_id={}&client_secret={}&code={}".format(client_id, client_secret, code)
    access_token = get_token(oAuthURL)
    return access_token, 200

