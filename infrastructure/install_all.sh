#!/bin/bash

echo "Enter your DNS Hostname (FQDN): "
read FQDN

echo "Enter your E-Mail address: "
read EMAIL

sed -i "s/__FQDN__/$FQDN/g" ingress_rules/fission_ingress.yaml
sed -i "s/__FQDN__/$FQDN/g" ingress_rules/ah-ah-ah_ingress.yaml

sed -i "s/__EMAIL__/$EMAIL/g" cert_manager/prod_issuer.yaml

curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable traefik" sh -
mkdir -p ~/.kube
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config

curl -LO https://get.helm.sh/helm-v3.5.1-linux-amd64.tar.gz
tar -xvf helm-v3.5.1-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/
rm -rf linux-amd64 helm-v3.5.1-linux-amd64.tar.gz
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update

export NGINX_NAMESPACE="ingress-nginx"
kubectl create namespace $NGINX_NAMESPACE
helm install --namespace $NGINX_NAMESPACE ingress-nginx stable/nginx-ingress \
    --set controller.kind=DaemonSet,controller.hostNetwork=true,controller.service.type=ClusterIP,rbac.create=true

kubectl apply --validate=false -f \ 
    https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager.yaml
kubectl -n cert-manager wait --for condition=Available --timeout=300s deploy/cert-manager-webhook
kubectl apply -f cert_manager/prod_issuer.yaml

export FISSION_NAMESPACE="fission"
kubectl create namespace $FISSION_NAMESPACE
helm install --namespace $FISSION_NAMESPACE --name-template fission \
    --set serviceType=ClusterIP,routerServiceType=ClusterIP \
    https://github.com/fission/fission/releases/download/1.11.2/fission-all-1.11.2.tgz

curl -Lo fission https://github.com/fission/fission/releases/download/1.11.2/fission-cli-linux
chmod a+x fission
sudo mv fission /usr/local/bin/

export AHAHAH_NAMESPACE="ah-ah-ah"
kubectl -n $AHAHAH_NAMESPACE apply --validate=false \ 
    https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.configmap.yaml
kubectl -n $AHAHAH_NAMESPACE apply --validate=false \ 
    https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.deployment.yaml
kubectl -n $AHAHAH_NAMESPACE apply --validate=false \ 
    https://raw.githubusercontent.com/c0dyhi11/ah-ah-ah/master/ah-ah-ah/ah-ah-ah.service.yaml

kubectl -n fission apply -f ingress_rules/fission_ingress.yaml
kubectl -n ah-ah-ah apply -f ingress_rules/ah-ah-ah_ingress.yaml

