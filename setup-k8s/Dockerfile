FROM ubuntu-debootstrap
# docker build -t setup-k8s .
# docker run -v ~/.ssh/:/root/.ssh/  setup-k8s
RUN apt-get update && apt install -y patch ssh curl git
WORKDIR /root
ENV KUBE_VERSION 1.5.0
RUN git clone --depth 1 https://github.com/kubernetes/kubernetes -b v$KUBE_VERSION kubernetes-$KUBE_VERSION
ENV KUBERNETES_PROVIDER ubuntu
ENV nodes "root@192.168.50.4"
ENV role_string "ai"
ENV NUM_MINIONS 1
ENV NUM_NODES 1
ENV SERVICE_CLUSTER_IP_RANGE 192.168.3.0/24
ENV FLANNEL_NET 172.16.0.0/16
ENV DEBUG true
COPY scripts /root/scripts
COPY a.patch /root
RUN cd kubernetes-$KUBE_VERSION && patch -p1 < /root/a.patch
RUN mkdir .ssh && chmod 700 .ssh
CMD cd /root && /root/scripts/up.sh
