# (cd /tmp/setup_volume && tar -czvf ../setup_volume.tar.gz .) && scp /tmp/setup_volume.tar.gz root@fs02:/export/share/kubernetes-app
set -x -e
DEST=/tmp/setup_volume
rm -fR $DEST
mkdir $DEST
cp -R \
    $GOPATH/src/github.com/tarasglek/k8s-vagrant \
    $GOPATH/src/github.com/purestorage/k8s-services \
    $GOPATH/src/github.com/PureStorage-OpenConnect/docker/cmd/k8s-provisioner \
    $GOPATH/src/github.com/PureStorage-OpenConnect/docker/cmd/pure-flex \
    $DEST
find $DEST -name .git |xargs rm -fR
(cd $DEST && ln -sv k8s-services/purestorage-k8s-services.py  k8s-services/config.json .)
SSH_HOST=root@fs66-b-app
# rsync -avz --delete $DEST/ $SSH_HOST:/setup/
ssh $SSH_HOST rm /setup/* -fR
tar -C $DEST -cz . | ssh $SSH_HOST tar -C /setup -zxv