from flask import request, Response
from flask import current_app


def main():
    html='<html><head><title>Install TV Show Request</title></head><body><a href="https://slack.com/oauth/v2/authorize?scope=incoming-webhook,commands,chat:write&client_id=643719483154.1373928919828"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a></body></html>'
    return Response(html, status=200, mimetype='text/html')

