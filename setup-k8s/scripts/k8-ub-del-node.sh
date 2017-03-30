#!/bin/bash

# This script deletes MINION node(s) defined in $del_nodes from an existing cluster.
# export del_nodes="root@ip.addr.1 root@ip.addr.2 root@ip.addr.3"
# Assumes k-vars.sh script has been run
# This script will stop, but NOT disable the services, remove files
# Assume sudo privileges to perform acctins

# Remove a minion node to a cluster


if [ -d "kubernetes-${KUBE_VERSION}/cluster" ]; then
 cd kubernetes-${KUBE_VERSION}/cluster
else #environment not K8 environment not set up
 echo "Run k-var.sh, K8 environment variables not set ..." >&2
 exit 1
fi

cd kubernetes-${KUBE_VERSION}/cluster
KUBE_ROOT=$(dirname "${BASH_SOURCE}")/..
export KUBECTL_PATH="${KUBE_ROOT}/cluster/ubuntu/binaries/kubectl"
export KUBE_CONFIG_FILE=${KUBE_CONFIG_FILE:-${KUBE_ROOT}/cluster/ubuntu/config-default.sh}
source "${KUBE_CONFIG_FILE}"
source "${KUBE_ROOT}/cluster/kube-env.sh"
source "${KUBE_ROOT}/cluster/kube-util.sh"


echo "Calling setClusterInfo ...">&2
setClusterInfo

echo "Deleting MINION nodes from the cluster with Master $MASTER_IP ...">&2


# used to track how many new nodes being added to the cluster
ii=0
new_node_str=""

for i in ${del_nodes};
  do
    #Don't schedule to this node

    echo Stopping services and deleting files on $i
    kubectl cordon ${i#*@}

   # drain pods and monitor that the pods are gone...
   # kubectl drain ${i#*@}


    ssh $SSH_OPTS -t "$i" "
          sudo -p '[sudo] password to stop node: ' -- /bin/bash -c '
            service kubelet stop 

            service kube-proxy stop

            service flanneld stop

            rm -rf /var/lib/kubelet
            '
          " || echo "Cleaning on node ${i#*@} failed"

    ssh $SSH_OPTS -t "$i" "sudo -- /bin/bash -c '
        rm -f \
          /opt/bin/kube* \
          /opt/bin/flanneld \
          /etc/init/kube* \
          /etc/init/flanneld.conf \
          /etc/init.d/kube* \
          /etc/init.d/flanneld \
          /etc/default/kube* \
          /etc/default/flanneld

        rm -rf ~/kube
        rm -f /run/flannel/subnet.env
      '" || echo "cleaning legacy files on ${i#*@} failed"

    echo Delete node ${i#*@} from the Master
    kubectl delete node ${i#*@}
done
