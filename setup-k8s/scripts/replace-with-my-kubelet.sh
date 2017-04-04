#!/bin/sh
set -x -e
DIR=/k8s/kubernetes-${KUBE_VERSION}
cd $DIR
./build-tools/run.sh make kubelet
for n in $nodes; do
    # avoid file is busy errors
    scp $DIR/_output/dockerized/bin/linux/amd64/kubelet $n:/tmp
    ssh $n mv /tmp/kubelet /opt/bin/kubelet
    # restart kubelet
    ssh $n killall kubelet
done