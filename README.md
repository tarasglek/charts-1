# Getting started

Setup http://github.com/PureStorage-OpenConnect/docker/cmd/k8s-provisioner/README.md

helm install --name p5555 postgresql-0.6.0.tgz --set persistence.storageClass=pure-provisioner,postgresPassword=taras,externalIP=10.19.66.145,port=5555
helm delete --purge p5555