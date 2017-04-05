#!/bin/sh
set -x -e
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDrh16eSSa8gieQlOcmkQZMTWyjdXXezph/MwsSypml62f8qDgEjXSNuFibr58JtWgODFkvj0G3yPVfUIjzdK1dt9oGNBpghX+HHtWMI5XaQz3Fl8dp/mUNL3Qy3wvbWuw4hhv8GnVyGe/y56nJrxcRT3wzXUcpI13NPGTZAhJ8nMXeZWfx3QFGui7dych4WQPmRpyUlbJeDUwzi4GJNSorSUl7Jnos4uYTxdShN6q1SVCKv9kI1tARLIP1422ic3dFWGIbw1p6eW3BBKN4crGSoDzdU1O9Ax6oXtfRZgGEQ6s3oFBzjPJkUUH9Yk//gKxJU9VkLxwtjg/Iv0U+ZmIp taras@taras-mbp >> /root/.ssh/authorized_keys

apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl linux-image-extra-$(uname -r) \

apt-get install -y xfsprogs open-iscsi multipath-tools util-linux socat

# instructions cut/pasted from https://kubernetes.io/docs/getting-started-guides/kubeadm/
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
# Install docker if you don't have it already.
apt-get install -y docker.io
apt-get install -y kubelet kubeadm kubectl kubernetes-cni

exit
# modify /etc/hosts to replace first 127.0.0.1 with 192.168.50.4 
kubeadm init --config /vagrant/kubeadm_config.yaml
cd /vagrant
mkdir -p ~/.kube && cp /etc/kubernetes/admin.conf ~/.kube/config && cp -R /root/.kube/ ~ubuntu/.kube/ && chown ubuntu:ubuntu -R ~ubuntu/.kube/
cp /root/.kube/config /vagrant/config
kubectl apply -f https://git.io/weave-kube-1.6
#enable scheduling pods on master node
kubectl taint nodes --all node-role.kubernetes.io/master-
# to make tiller work: curl https://gist.githubusercontent.com/groundnuty/fa778fc06cd79f4de687490afb6de421/raw/b43e3a4c1f2670f038db9415cc7f90b2efd3eab5/serviceaccount_fix.yaml  | kubectl --kubeconfig /etc/kubernetes/admin.conf create -f -
# kubectl get --all-namespaces pods
#ip -o address show dev enp0s8
#