#!/bin/bash

# This script provisions new node(s) defined in $add_nodes and adds it to an existing cluster.
# export add_nodes="root@ip.addr.1 root@ip.addr.2 root@ip.addr.3"
# Assumes k-vars.sh script has been run
# This script will call the functions to download the software to the node and add it to the cluster.
#

# Add a minion node to a cluster

if [ -d "kubernetes-${KUBE_VERSION}/cluster" ]; then
 cd kubernetes-${KUBE_VERSION}/cluster
else #environment not K8 environment not set up
 echo "Run k-var.sh, K8 environment variables not set ..." >&2
 exit 1
fi

KUBE_ROOT=$(dirname "${BASH_SOURCE}")/..
export KUBECTL_PATH="${KUBE_ROOT}/cluster/ubuntu/binaries/kubectl"
export KUBE_CONFIG_FILE=${KUBE_CONFIG_FILE:-${KUBE_ROOT}/cluster/ubuntu/config-default.sh}
source "${KUBE_CONFIG_FILE}"
source "${KUBE_ROOT}/cluster/kube-env.sh"
source "${KUBE_ROOT}/cluster/kube-util.sh"

# downloading tarball release
"${KUBE_ROOT}/cluster/ubuntu/download-release.sh"

echo "Calling setClusterInfo ...">&2 
setClusterInfo

echo "Adding nodes to the cluster with Master $MASTER_IP ...">&2

echo "#!/bin/bash" > $HOME/new_kube_var.sh
chmod +x $HOME/new_kube_var.sh

# used to track how many new nodes being added to the cluster
ii=0
new_node_str=""
 
for i in ${add_nodes}
  do
    {
	# TODO: May want to blow installed docker away or check version...
	echo Checking if docker already runnning on
        if ssh $i  pgrep docker > /dev/null
        then
            echo "Docker is running ...">&2
        else
            echo "Installing Docker on $i" >&2
            ssh $i "curl -sSL https://get.docker.com/ | sh"
        fi
    
	ssh $i docker run -rm hello-world

	echo "provision-node $i">&2
	provision-node "$i"
	new_node_str="$new_node_str i"
	((ii=ii+1))
    }
  done

echo "export role_string=\"$role_string $new_node_str\""  >> $HOME/new_kube_var.sh
echo "export NUM_NODES=$(($NUM_NODES+$ii))"  >> $HOME/new_kube_var.sh
echo "export NUM_MINIONS=$(($NUM_MINIONS+$ii))" >> $HOME/new_kube_var.sh
echo "export nodes=\"$nodes $add_nodes\""  >> $HOME/new_kube_var.sh
echo source $HOME/new_kube_var.sh to update K8 environment variables

# need to give the node some time to start, this may not be enough time...
sleep 10 
echo Listing nodes in the cluster
kubectl get nodes

