#!/usr/bin/env python
import subprocess
import sys
import re

def run(cmd):
    print cmd
    sys.stdout.flush()
    return subprocess.check_output(cmd, shell=True)

def list_pg():
    helm_output = run("helm list").split("\n")
    for line in helm_output[1:]:
        cols = line.split("\t")
        name = cols[0]
        m = re.search(r'^p(\d+)$', name)
        if not m:
            # print "(%s) is not a db volume, skipping" % (name)
            continue
        yield (name, int(m.group(1)))

def provision_another():
    new_port = 5432
    print sys.argv
    for (pg, port) in list_pg():
        new_port = max(new_port, port + 1)
    run("helm install --name p{port} postgresql-0.6.0.tgz --set persistence.storageClass=pure-provisioner,postgresPassword=taras,externalIP=10.19.66.145,port={port}".format(port=new_port))

def delete_all():
    for (pg, port) in list_pg():
        run("helm delete --purge " + pg)

def main():
    if sys.argv[1:] == ["--delete-all"]:
        delete_all()
    else:
        provision_another()

main()
