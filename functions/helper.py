import time
import hmac
import hashlib


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


def verify_request(slack_signing_secret, request_body, timestamp,
                   slack_signature):
    if abs(time.time() - float(timestamp)) > 60 * 5:
        return False
    sig_basestring = 'v0:%s:%s' % (timestamp, request_body)
    my_signature = 'v0=%s' % (hmac.new(slack_signing_secret.encode('utf-8'),
                                       sig_basestring.encode('utf-8'),
                                       digestmod=hashlib.sha256).hexdigest())
    if hmac.compare_digest(my_signature, slack_signature):
        return True
    else:
        return False

