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

def provision_one(port):
    run("helm install --name p{port} postgresql-0.6.0.tgz --set persistence.storageClass=pure-provisioner,postgresPassword=taras,externalIP=10.19.66.145,port={port}".format(port=port))
    
def provision_another():
    new_port = 5432
    print sys.argv
    for (pg, port) in list_pg():
        new_port = max(new_port, port + 1)
    provision_one(new_port)

def delete_all():
    for (pg, port) in list_pg():
        run("helm delete --purge " + pg)

def main():
    args = sys.argv[1:]
    if args == ["--delete-all"]:
        delete_all()
    elif len(args) == 2 and args[0] == "--port":
        provision_one(int(args[1]))
    else:
        provision_another()

main()
