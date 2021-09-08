import json
import requests
import urllib.parse
from helper import fetch_kube_data, verify_request
from flask import request, Response
from flask import current_app


def slack_webhook(url, payload):
    headers = {'Accept': 'application/json',
               'Content-type': 'application/json'}
    message = {"text": payload}
    rest_call = requests.post(url, headers=headers, data=json.dumps(message))
    return rest_call.text


def add_show(url, show_name, show_id):
    headers = {'Accept': 'application/json'}
    url += "show.addnew"
    url += "&status=wanted"
    url += "&future_status=wanted"
    url += "&initial=hdtv|hdwebdl|hdbluray"
    url += "&indexerid={}".format(show_id)
    url += "&location=/Media/Video/TV Shows"
    rest_call = requests.get(url, headers=headers)
    return json.loads(rest_call.text)


def main():
    slack_signing_secret = fetch_kube_data("secret", "default", "slackbot", "signing-secret")
    #sickchill_url = fetch_kube_data("secret", "default", "slackbot", "sickchill-url")
    slack_url = fetch_kube_data("secret", "default", "slackbot", "slack-url")
    sickchill_url = 'http://192.168.170.44:8081/api/e48b93bf3e0e3bfc253250e7b761b3b4/?cmd='
    try:
        timestamp = request.headers['X-Slack-Request-Timestamp']
        slack_signature = request.headers['X-Slack-Signature']
        request_body = request.get_data().decode('utf-8')
    except:
        return "Unauthorized", 200

    if not verify_request(slack_signing_secret, request_body, timestamp, slack_signature):
        return "Unauthorized", 200

    json_payload = json.loads(urllib.parse.unquote_plus(request_body)[8:])
    current_app.logger.info(json.dumps(json_payload))
    show = json_payload['actions'][0]['selected_option']['value']
    if show[0:6] == "cancel":
        return "ok", 200
    show_name, show_id = show.split("|")
    show_id = int(show_id)
    sickchill_result = add_show(sickchill_url, show_name, show_id)
    message = "{}: {}".format(sickchill_result['result'], sickchill_result['message'])
    result = slack_webhook(slack_url, message)
    return result, 200


if __name__ == "__main__":
    main()

