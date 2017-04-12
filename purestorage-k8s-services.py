#!/usr/bin/python
"""
This script lives in /mnt(of k8s-meta partition)
It sets up iscsi networking(purenetwork can't do that yet) and does initial k8s config
"""

import sys
import os
import os.path
import subprocess


MY_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
ISCSI_IP_SET = {
    "data4": "10.15.66.9",
    "data5": "10.15.66.10"
}

def run(cmd):
    print cmd
    sys.stdout.flush()
    try:
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(err.output)
        raise err

def main():
    for interface, ip in ISCSI_IP_SET.iteritems():
        run("ifconfig {interface} {ip} netmask 255.255.255.0 up".format(ip=ip, interface=interface))
    if os.path.exists("/etc/kubernetes/admin.conf"):
        sys.exit(0)
    run("kubeadm init --pod-network-cidr 10.244.0.0/16")
    # enable kubectl to run locally
    print run("mkdir -p ~/.kube && cp /etc/kubernetes/admin.conf ~/.kube/config")
    # flannel + rbac permissions
    run("cd %s/k8s-vagrant && ./k8s_config.sh" % MY_DIR)
    # install pure provisioner
    run("cd %s/k8s-provisioner && ./install_local.sh" % MY_DIR)

main()
