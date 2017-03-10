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
