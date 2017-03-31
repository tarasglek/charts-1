#!/bin/bash
#run cluster/kube-up.sh, need to be root?
if [ -d "kubernetes-${KUBE_VERSION}/cluster" ]; then
 cd kubernetes-${KUBE_VERSION}/cluster
else #environment not K8 environment not set up
 echo "Run k-var.sh, K8 environment variables not set ..." >&2
 exit 1
fi

cd kubernetes-${KUBE_VERSION}/cluster
./kube-up.sh

#error checking for cluster

# verify cluster is up
kubectl cluster-info
kubectl get nodes
# Check output of kubectl commands

# Now that we have the base cluster up, deploy dns and ui
# these are supplied as addons in the kubernetes tarball
cd ubuntu
./deployAddons.sh
