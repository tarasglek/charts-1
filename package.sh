set -x -e
DEST=$GOPATH/src/github.com/purestorage/k8s-services/config_volume
rm -fR $DEST
mkdir $DEST
cp -Rv $GOPATH/src/github.com/purestorage/k8s-services/purestorage-k8s-services.py \
    $GOPATH/src/github.com/tarasglek/k8s-vagrant \
    $GOPATH/src/github.com/PureStorage-OpenConnect/docker/cmd/k8s-provisioner \
    $DEST

find $DEST -name .git |xargs rm -fR

rsync -avz --delete $DEST/ root@fs66-b-app:/mnt