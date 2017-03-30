#!/bin/bash

if [ -d "kubernetes-${KUBE_VERSION}/cluster" ]; then
 cd kubernetes-${KUBE_VERSION}/cluster
else #environment not K8 environment not set up
 echo "Run k-var.sh, K8 environment variables not set ..." >&2
 exit 1
fi

cd kubernetes-${KUBE_VERSION}/cluster
./kube-down.sh

