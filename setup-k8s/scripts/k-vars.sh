#!/bin/bash
me=`whoami`
export PATH=$PATH:/root/kubernetes-${KUBE_VERSION}/cluster/ubuntu/binaries
export KUBERNETES_PROVIDER=ubuntu
export nodes="root@192.168.50.4"
export role_string="ai"
export NUM_MINIONS=1
export NUM_NODES=1
export SERVICE_CLUSTER_IP_RANGE=192.168.3.0/24
export FLANNEL_NET=172.16.0.0/16
export DEBUG=true
export BASH_DEBUG_FLAGS="set -x"
