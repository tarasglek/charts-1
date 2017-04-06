#!/bin/sh
set -x -e
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDrh16eSSa8gieQlOcmkQZMTWyjdXXezph/MwsSypml62f8qDgEjXSNuFibr58JtWgODFkvj0G3yPVfUIjzdK1dt9oGNBpghX+HHtWMI5XaQz3Fl8dp/mUNL3Qy3wvbWuw4hhv8GnVyGe/y56nJrxcRT3wzXUcpI13NPGTZAhJ8nMXeZWfx3QFGui7dych4WQPmRpyUlbJeDUwzi4GJNSorSUl7Jnos4uYTxdShN6q1SVCKv9kI1tARLIP1422ic3dFWGIbw1p6eW3BBKN4crGSoDzdU1O9Ax6oXtfRZgGEQ6s3oFBzjPJkUUH9Yk//gKxJU9VkLxwtjg/Iv0U+ZmIp taras@taras-mbp >> /root/.ssh/authorized_keys

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -L
# ip route add 192.168.50.0/8 dev enp0s8

apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl linux-image-extra-$(uname -r) \

apt-get install -y xfsprogs open-iscsi multipath-tools util-linux socat python

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


#fix env
# need kubeadm with https://github.com/kubernetes/kubernetes/pull/43835/files
# cp /vagrant/kubeadm-1.6.fixed /usr/bin/kubeadm
/vagrant/swap_etc_hosts_run_kubeadm.py
