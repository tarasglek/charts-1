#!/bin/bash
#
# This script assumes the kubernetes cluster env variables are set (using k-vars.sh).
# This installs docker on all the machines in the cluster defined in $nodes.
# There is no error handling or checking.
# This is required for Ubuntu installs and will be deprecated with ReOS.
#

# Check is $nodes is set and if set, not an empty string
  if [ -z $nodes ]; then
	echo "Environment variable \$nodes not set or is an empty string! Run k-vars.sh first!"
	exit 1
  fi

  for i in $nodes; do
    echo "Installing Docker on $i" >&2
    ssh $i "curl -sSL https://get.docker.com/ | sh"
    echo "Verifying Docker install on $i" >&2 
    ssh $i docker run --rm hello-world
      
  done
