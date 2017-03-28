# Getting started

Setup http://github.com/PureStorage-OpenConnect/docker/cmd/k8s-provisioner/README.md

helm install --name p5555 postgresql-0.6.0.tgz --set persistence.storageClass=pure-provisioner,postgresPassword=taras,externalIP=10.19.66.145,port=5555
helm delete --purge p5555

# Issues
* Currently I have a volume that doesn't pass fsck. See output in describe.completed.error.txt
** Need a state machine to handle recovery for fs-level errors and higher-level pg ones
** Seems that RDS gives up and expects users to do PITR recovery https://news.ycombinator.com/item?id=4115937guestmount -a 
