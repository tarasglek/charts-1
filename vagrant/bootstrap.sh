#!/bin/sh
set -x -e
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDrh16eSSa8gieQlOcmkQZMTWyjdXXezph/MwsSypml62f8qDgEjXSNuFibr58JtWgODFkvj0G3yPVfUIjzdK1dt9oGNBpghX+HHtWMI5XaQz3Fl8dp/mUNL3Qy3wvbWuw4hhv8GnVyGe/y56nJrxcRT3wzXUcpI13NPGTZAhJ8nMXeZWfx3QFGui7dych4WQPmRpyUlbJeDUwzi4GJNSorSUl7Jnos4uYTxdShN6q1SVCKv9kI1tARLIP1422ic3dFWGIbw1p6eW3BBKN4crGSoDzdU1O9Ax6oXtfRZgGEQ6s3oFBzjPJkUUH9Yk//gKxJU9VkLxwtjg/Iv0U+ZmIp taras@taras-mbp >> /root/.ssh/authorized_keys
apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"

apt-get update
# install various goodies for kubernetes
apt-get -y install docker-ce xfsprogs open-iscsi multipath-tools util-linux socat
# install nsenter for helm(tiller)
docker run --rm -v /usr/local/bin:/target jpetazzo/nsenter