# Getting started

Setup k8s as pure app per https://wiki.purestorage.com/display/psw/Kubernetes+App

Checkout this repository into pure app vm.
```
> ./introducer.py  --install
> POSTGRES_IP=`kubectl get nodes -o jsonpath='{.items[*].status.addresses[].address}'` && echo $POSTGRES_IP
```

Now create volumes using db-### where ### is a number in k8s nodePort range (default 30000-32767). Attach these to your pure app.

This will result in introducer.py spinning up database instances.

```
# Connect from another computer on lan
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
