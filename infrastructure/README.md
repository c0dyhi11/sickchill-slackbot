# Infrastructure
This will outline the infrastructure needed to deploy this SlackBot.

## Prerequisites 

### [Slack](https://api.slack.com)
You will need a slack account and setting up the slack side of things will not be documented here yet...

### [SickChill](https://github.com/SickChill/SickChill)
You will need SickChill setup and working. The documentation to set this up won't be provided here.

### [Linux System](https://www.linux.org)
I will be using and x86 [Ubuntu 20.04](https://releases.ubuntu.com/20.04/) in this example. Some of the software I'm using is not compiled for ARM processors so a Raspberry Pi won't work. All scripts provided will assume you are using [Ubuntu 20.04](https://releases.ubuntu.com/20.04/) on an x86 system as well.

### Public IP Address
This can be port forwarded from you router to the Ingress Controller IP. But you will at minimum need port 80 and 443 open to your Linux System.

### DNS Name
You will need a DNS name statically set to your Public IP above. This will be used to get an SSL cert issued vie Lets Encrypt. If you don't have one go to [GoDaddy](https://godaddy.com) or [NameCheap](https://namecheap.com) an register a .com domain for about $15 a year. There are normally promo pricing for new domains so you can find it cheaper than this as well. Once you do this create a host DNS record like slackbot.mydomain.tld and point it to your Public IP Address.

### Clone this repo
You will need to install git and need to clone this repo to your Ubuntu machine and navigate into the infrastructure directory

To do this run the following commands:
```bash
sudo apt-get update -y
sudo apt-get install git -y
cd ~
git clone https://github.com/c0dyhi11/sickchill-slackbot.git
cd ~/sickchill-slackbot/infrastructure
```

## TL; DR
If you don't care about how the infrastructure is deployed. Just run the following script on an Ubuntu 20.04 machine and move on to setting up your SlackBot.

I'm assuming you have already cloned this git repo and you are in the `Infrastructure` directory.
```bash
bash install_all.sh
```
## Manual Install

### [Kubernetes](https://kubernetes.io)
We will be using [k3s](https://k3s.io) in this example, and I'm going to replace the ingress controller with Nginx because I'm lazy and don't want to learn traefik.

To install k3s run the following commanda:
```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable traefik" sh -
mkdir -p ~/.kube
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

### [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)
You will need kubectl to manage your kubernetes cluster.

To install kubectl run the following command:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod a+x kubectl
sudo mv kubectl /usr/local/bin/
```

### [Helm](https://helm.sh)
You will need to install the Helm CLI tool in order to install other Kubernetes applications.

To install helm run the following commands:
```bash
curl -LO https://get.helm.sh/helm-v3.5.1-linux-amd64.tar.gz
tar -xvf helm-v3.5.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/
rm -rf linux-amd64 helm-v3.5.1-linux-amd64.tar.gz
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

### [Nginx-Ingress](https://kubernetes.github.io/ingress-nginx/)
We are using the Nginx Ingress Controller because I'm very lazy and don't want to update my ingress rules for traefik.

To install the Nginx Ingress Controller run the following commands:
```bash 
export NGINX_NAMESPACE="ingress-nginx"
kubectl create namespace $NGINX_NAMESPACE
helm install --namespace $NGINX_NAMESPACE ingress-nginx stable/nginx-ingress \
    --set controller.kind=DaemonSet,controller.hostNetwork=true,controller.service.type=ClusterIP,rbac.create=true
```

### [Cert Manager](https://cert-manager.io/docs/)
Cert Manager will automate the creation and renewal of SSL certificates for your domain.

***You will need to edit `prod_issuer.yaml` and repalce `__EMAIL__` with you actual email address.***

To install Cert Manager run the following commands:
```bash
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager.yaml
kubectl -n cert-manager wait --for condition=Available --timeout=300s deploy/cert-manager-webhook
kubectl apply -f cert_manager/prod_issuer.yaml
```

### [Fission](https://fission.io)
Fission is a Serverless framework or "Functions as a Service" platform. This entire SlackBot is broken into multiple small functions.

To install Fission run the following commands:
```bash
export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
helm install --namespace $FISSION_NAMESPACE --name-template fission \
    --set serviceType=ClusterIP,routerServiceType=ClusterIP \
    https://github.com/fission/fission/releases/download/1.11.2/fission-all-1.11.2.tgz
```

### [Fission-CLI](https://docs.fission.io/docs/installation/#install-fission-cli)
You will also need to install the Fission CLI to interact with Fission

To install the Fission CLI run the following commands:
```bash
curl -Lo fission https://github.com/fission/fission/releases/download/1.11.2/fission-cli-linux
chmod a+x fission
sudo mv fission /usr/local/bin/
```

### [Ah-Ah-Ah](https://github.com/c0dyhi11/ah-ah-ah/tree/master/ah-ah-ah)
This app is used as a landing zone to redirect an insecure endpoint from Fission when exposing Fission publicly.

To deploy Ah-Ah-Ah run the following commands:
```bash
export AHAHAH_NAMESPACE="ah-ah-ah"
kubectl -n $AHAHAH_NAMESPACE apply --validate=false https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.configmap.yaml
kubectl -n $AHAHAH_NAMESPACE apply --validate=false https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.deployment.yaml
kubectl -n $AHAHAH_NAMESPACE apply --validate=false https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.service.yaml
```

### [Ingress Rules](https://kubernetes.io/docs/concepts/services-networking/ingress/)
We will need two kubernetes ingress rules.
* One for will be used for all of the fission traffic.
* The second will be used to block the /fission-functions/ endpoint from fission and redirect it to ah-ah-ah because this endpoint shouldn't be accessible from the public.

***You will need to edit both ingress files and replace `__FQDN__` with you actual DNS hostname for your server.***

To apply these ingress rules run the following commands:
```bash
kubectl -n fission apply -f ingress_rules/fission_ingress.yaml
kubectl -n ah-ah-ah apply -f ingress_rules/ah-ah-ah_ingress.yaml
```

## Done!
You are now ready to deploy the functions!

You'll find those instructions in the [`functions`](https://github.com/c0dyhi11/sickchill-slackbot/tree/master/functions) directory in this same repository.

