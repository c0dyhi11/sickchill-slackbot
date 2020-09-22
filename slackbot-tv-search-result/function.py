import json
import requests
import urllib.parse
from flask import request, Response
from flask import current_app


def get_search_results(url, search_text):
    headers = {'Accept': 'application/json'}
    print(search_text)
    url += urllib.parse.quote(search_text)
    rest_call = requests.get(url, headers=headers)
    return json.loads(rest_call.text)


def build_message(shows, search_text, user):
    url_prefix = 'https://www.thetvdb.com/?tab=season&seriesid='
    payload = json.loads("""
                            {
                              "blocks": [
                                {
                                  "type": "header",
                                  "text": {
                                    "type": "plain_text",
                                    "text": "",
                                    "emoji": true
                                  }
                                },
                                {
                                  "type": "section",
                                  "block_id": "section1",
                                  "text": {
                                    "type": "mrkdwn",
                                    "text": ""
                                  }
                                },
                                {
                                  "type": "divider"
                                },
                                {
                                  "type": "section",
                                  "text": {
                                    "type": "mrkdwn",
                                    "text": "Select a show from above to add:"
                                  },
                                  "accessory": {
                                    "type": "static_select",
                                    "placeholder": {
                                      "type": "plain_text",
                                      "text": "Select a show",
                                      "emoji": false
                                    },
                                    "options": []
                                  }
                                }
                              ]
                            }
                        """)
    text_header = "Here are the search results for: {}".format(search_text)
    text_body = "@{}\n".format(user)
    options = []
    show_results = shows['data']['results']
    sort_shows_by_name = sorted(show_results, key=lambda i: i['name'])
    sort_shows_by_attainment = sorted(sort_shows_by_name,
                                      key=lambda i: i['in_show_list'],
                                      reverse=True)
    downloadable_show = False
    for show in sort_shows_by_attainment:
        if show['in_show_list']:
            text_body += ":warning:   <{}{}|{}>   ({})   `[Already Added]`\n".format(url_prefix, str(show['tvdbid']), show['name'], show['first_aired'])
        else:
            downloadable_show = True
            text_body += ":large_blue_circle:   <{}{}| {}>   ({})\n".format(url_prefix, str(show['tvdbid']), show['name'], show['first_aired'])
            options.append({"text": {
                                "type": "plain_text",
                                "text": "{}   ({})".format(show['name'], show['first_aired']),
                                "emoji": False
                            },
                            "value": str(show['tvdbid'])})
    options.append({"text": {
                    "type": "plain_text",
                    "text": "*Cancel*",
                    "emoji": False},
                "value": "cancel"
                })
    payload['blocks'][3]['accessory']['options'] = options
    if len(text_body) >= 3000:
        text_body = "@{}\n:x:   There were far too many results for your search term: *{}*.\nPlease add words to narrow your search!".format(user, search_text)
        downloadable_show = False
    elif len(sort_shows_by_attainment) == 0:
        text_body += ":x:   We were unable to find any TV Shows matching the text: *{}*\n Please try searching again with different keywords.".format(search_text)
    if not downloadable_show:
        del payload['blocks'][3]
        del payload['blocks'][2]
    payload['blocks'][0]['text']['text'] = text_header
    payload['blocks'][1]['text']['text'] = text_body
    return payload


def slack_webhook(url, payload):
    headers = {'Accept': 'application/json',
               'Content-type': 'application/json'}
    print(json.dumps(payload))
    rest_call = requests.post(url, headers=headers, data=json.dumps(payload))
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
    sickchill_url = fetch_kube_data("secret", "default", "slackbot", "sickchill-url")
    slack_url = fetch_kube_data("secret", "default", "slackbot", "slack-url")

    request_body = json.loads(request.get_data().decode('utf-8'))
    search_text = request_body['text']
    user = request_body['user']

    search_result = get_search_results(sickchill_url, search_text)
    slack_message = build_message(search_result, search_text, user)
    webhook_result = slack_webhook(slack_url, slack_message)

    return webhook_result, 200


if __name__ == "__main__":
    main()

