# Getting started

```
> minikube start
```
A pod is just a set of containers
Deployment is a pod managed by replicasets


```
> kubectl create -f hostpath-pv.yaml
> kubectl create -f hostpath-pvc.yaml
> kubectl create -f postgres-service.yaml
> kubectl create -f postgres.yaml
# Get node addresses
> POSTGRES_IP=`kubectl get nodes -o jsonpath='{.items[*].status.addresses[].address}'` && echo $POSTGRES_IP
# Connect
> psql -h $POSTGRES_IP -p 30432 -U postgres
```
# Troubleshooting
```
> kubectl describe pods
# this can give FailedScheduling
> kubectl describe nodes
# this can return "Cannot connect to Docker daemon(lol)
```

# StorageClass

minikube has an annoying default storageclass that satisfies all claims via hostpath. The following gets rid of that
```
> kubectl get storageclass
NAME                 TYPE
standard (default)   k8s.io/minikube-hostpath
> kubectl delete storageclass --all
storageclass "standard" deleted
```
