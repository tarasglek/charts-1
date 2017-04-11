#!/usr/bin/env python
import subprocess
import sys
import re

def run(cmd):
    print cmd
    sys.stdout.flush()
    try:
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(err.output)
        raise err

def list_pg():
    try:
        helm_output = run("helm list").split("\n")
    except subprocess.CalledProcessError:
        run("helm init #maybe try again once tiller has been activated")
        sys.exit(0)

    for line in helm_output[1:]:
        cols = line.split("\t")
        name = cols[0]
        m = re.search(r'^p(\d+)$', name)
        if not m:
            # print "(%s) is not a db volume, skipping" % (name)
            continue
        yield (name, int(m.group(1)))

def get_external_ip():
    yaml = run("kubectl get nodes --output=yaml")
    ip = yaml.split("- address: ")[1].split("\n")[0]
    return ip

def provision_one(port, provisioner):
    ip = get_external_ip()
    run("helm install --name p{port} postgresql-0.6.0.tgz --set persistence.storageClass={provisioner},postgresPassword=taras,externalIP={ip},port={port}".format(port=port, ip=ip, provisioner=provisioner))

def provision_another(port=5432, provisioner="pure-provisioner"):
    new_port = port
    print sys.argv
    for (pg, port) in list_pg():
        new_port = max(new_port, port + 1)
    provision_one(new_port, provisioner)

def delete_all():
    for (pg, port) in list_pg():
        run("helm delete --purge " + pg)

def main():
    args = sys.argv[1:]
    if args == ["--delete-all"]:
        delete_all()
    elif len(args) == 2:
        if args[0] == "--port":
            provision_another(port=int(args[1]))
        elif args[0] == "--provisioner":
            provision_another(provisioner=args[1])
    else:
        provision_another()

main()
