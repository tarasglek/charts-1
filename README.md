# Getting started

```
> minikube start
```
A pod is just a set of containers
Deployment is a pod managed by replicasets


# Admin
```
> kubectl create -f empty-set-pod.yaml
> kubectl get pods
NAME                   READY     STATUS    RESTARTS   AGE
empty-set-pod   0/1       Pending   0          1m
> kubectl describe pods
# run bash
> kubectl exec -ti empty-set-pod bash 
 ```
# Troubleshooting
```
> kubectl describe pods
# this can give FailedScheduling
> kubectl describe nodes
# this can return "Cannot connect to Docker daemon(lol)
```
# Log

March 9: Use an emptyVol mount to serve a persistent volume via NFS

# NFS

```console
$ kubectl create -f nfs/nfs-server-rc.yaml
$ kubectl create -f nfs/nfs-server-service.yaml
# get the cluster IP of the server using the following command
$ NFS_IP=`kubectl describe services nfs-server|grep IP:|sed 's/[^0-9]*//'` && echo $NFS_IP
# use the NFS server IP to update nfs-pv.yaml and execute the following
$ sed 's/\( *server: \)\(.*\)/\1'$NFS_IP'/' nfs/nfs-pv.yaml.template > nfs/nfs-pv.yaml 
$ kubectl create -f nfs/nfs-pv.yaml
$ kubectl create -f nfs/nfs-pvc.yaml
# run postgres
$ kubectl create -f postgres.yaml
```

