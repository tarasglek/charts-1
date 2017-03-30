# scripts
Bash scripts for an Ubuntu K8 cluster (ToBeDeprecated by ReOS)
Assumes passwordless ssh root access needs to be setup for the scripts that perform remote ops (all be k-vars.sh)
k-vars.sh: K8 environment variables and cluster IPs ($nodes)
installDocker.sh: install latest docker on cluster IPS ($nodes)
up.sh: creates and starts K8 cluster on $nodes and other details specified in environment by k-vars.sh
down.sh: stop/tear down K8 cluster on $nodes
k8-ub-add-ndoe.sh: add MINION $add_nodes to current K8 cluster, creates shell script to update environment variables
k8-ub-del-node.sh: remove minion $del_nodes from current K8 cluster, waiting on POD evac is NYI

current K8 cluster is defined in ~/.kube/config