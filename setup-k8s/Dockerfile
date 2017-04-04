FROM ubuntu-debootstrap
# docker build -t setup-k8s .
# docker run -v /var/run/docker.sock:/var/run/docker.sock -v ~/.ssh/:/root/.ssh/ -v `pwd`:/root/.kube/ -v `pwd`/scripts:/k8s/scripts/ setup-k8s
RUN apt-get update && apt-get install -y apt-transport-https  ca-certificates  curl  software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    apt-key fingerprint 0EBFCD88 && \
    add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" && \
   apt-get update && \
   apt-get install -y docker-ce ssh git
RUN mkdir /k8s
WORKDIR /k8s
ENV KUBE_VERSION 1.5.0
RUN git clone --depth 1 https://github.com/tarasglek/kubernetes kubernetes-$KUBE_VERSION -b taras
ENV KUBERNETES_PROVIDER ubuntu
ENV nodes "root@192.168.50.4"
# root@192.168.50.5 root@192.168.50.6"
ENV role_string "ai"
# i i"
#ENV NUM_MINIONS 3
#ENV NUM_NODES 3
ENV NUM_NODES 1
ENV SERVICE_CLUSTER_IP_RANGE 192.168.3.0/24
ENV FLANNEL_NET 172.16.0.0/16
ENV DEBUG true
RUN echo 'export PATH=/k8s/kubernetes-'${KUBE_VERSION}'/cluster/ubuntu/binaries:$PATH' >> /etc/profile
RUN mkdir ~/.ssh && chmod 700 ~/.ssh && mkdir ~/.kube
COPY scripts /k8s/scripts
# ./build-tools/run.sh  make KUBE_FASTBUILD=true ARCH=amd64
CMD cd /k8s && \
    /k8s/scripts/up.sh 
    #&& \
    #/k8s/scripts/replace-with-my-kubelet.sh