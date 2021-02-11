# sickchill-slackbot
This is a Slackbot desinged to allow the ability to add shows to sickchill, sickbeard, and/or sickrage. It is built on top of the Fission Serverless Framework

## TODO
### We should be using repsonse URLs and delete source messages: 
https://api.slack.com/interactivity/handling#updating_message_response

https://api.slack.com/interactivity/handling#deleting_message_response


### Write a doc on this: Kubernetes Secret
You will need to create a k8s secret with the following data.
```bash
kubectl -n default create secret generic slackbot \
--from-literal=client-id='123456789012.3456789012345' \
--from-literal=client-secret='as7234ikds92d723d78cc8ht0934ld79' \
--from-literal=sickchill-url='http://192.168.1.10:8081/api/0fs34njksd6g8vdfjouilk907jk65439/?cmd=sb.searchtvdb&lang=en&only_new=0&name=' \
--from-literal=signing-secret='jkn32487dfvyh542thby423r579vefsb' \
--from-literal=slack-url='https://hooks.slack.com/services/DS743FRE7/2317CDEN43J/2379DESEFCVsdah0ASDJADdj'
```

I'm not sure where all of this data is found yet. But I'm pretty sure when create a slack app you'll find everything but the `sickchill-url`
