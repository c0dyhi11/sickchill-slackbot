import json
import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
from flask import request, Response
from flask import current_app
from helper import fetch_kube_data, verify_request


async def publish_message(loop, subject, payload,
                          url='nats://defaultFissionAuthToken@nats-streaming.fission:4222',
                          cluster_id='fissionMQTrigger', client_id='fission-python-function'):
    nc = NATS()
    await nc.connect(url, loop=loop)
    sc = STAN()
    await sc.connect(cluster_id, client_id, nats=nc)
    await sc.publish(subject, payload.encode('UTF-8'))
    await sc.close()
    await nc.close()


def main():
    slack_signing_secret = fetch_kube_data("secret", "default", "slackbot", "signing-secret")
    try:
        timestamp = request.headers['X-Slack-Request-Timestamp']
        slack_signature = request.headers['X-Slack-Signature']
        request_body = request.get_data().decode('utf-8')
    except:
        return "Unauthorized", 200

    if not verify_request(slack_signing_secret, request_body, timestamp, slack_signature):
        return "Unauthorized", 200

    nats_subject = 'tv-request'
    nats_payload = {}
    nats_payload['user'] = request.form.get('user_name')
    nats_payload['text'] = request.form.get('text')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(publish_message(loop, nats_subject, json.dumps(nats_payload)))
    loop.close()

    message = "We'll Look for TV Show: *%s*!" % nats_payload['text']

    return message, 200


if __name__ == "__main__":
    main()

