#!/usr/bin/python
"""
This script lives in /mnt(of k8s-meta partition)
It sets up iscsi networking(purenetwork can't do that yet) and does initial k8s config

mount /setup -o remount,rw ;cd ~ && nc -l -p 9000|tar -xv && chown root:root -R .ssh
tar -C ~ -c .ssh/authorized_keys|nc fs66-b-app 9000
"""

import sys
import os
import os.path
import subprocess
import json

MY_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
CONFIG_FILE = MY_DIR + "/config.json"
CONFIG = json.loads(open(CONFIG_FILE).read())

def run(cmd):
    print cmd
    sys.stdout.flush()
    try:
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as err:
        sys.stderr.write(err.output)
        raise err

stopped_docker = False
docker_data_dir = '/data/docker'
docker_lib_dir = '/var/lib/docker'

def stop_docker():
    global stopped_docker
    if stopped_docker:
        return
    run("systemctl stop docker")
    #docker likes to fail to unmount stuff
    run("umount  -l /data/docker/aufs || true")
    stopped_docker = True

def maybe_stop_docker(srcdir):
    if srcdir in [docker_data_dir, docker_lib_dir]:
        stop_docker()

def ensure_symlink(src, dest, force=False):
    # if dest dir exists
    delete_preexisting = False
    need_to_create_link = True
    try:
        # delete if symlink points at wrong dest
        readlink = os.readlink(src)
        need_to_create_link = readlink != dest
        # readlink succeeded, but it doesn't point to right place
        delete_preexisting = need_to_create_link
    except OSError as err:
        # 22 Invalid argument, means something exists, but isn't a link
        delete_preexisting = err.errno == 22
    if need_to_create_link:
        maybe_stop_docker(src)
    if delete_preexisting:
        run("rm -r " + src)
    if need_to_create_link:
        force_flag = "-f" if force else ""
        create_cmd = "ln -s {force_flag} {dest} {src}".format(src=src,
                                                              dest=dest, force_flag=force_flag)
        try:
            run(create_cmd)
        except:
            run("mkdir -p {parent} && {create_cmd}".format(
                parent=os.path.dirname(src), create_cmd=create_cmd))

# Validate and/or create symlinks for k8s state
def separate_state():
    from stat import ST_MODE, S_ISDIR, S_ISLNK
    # got this list of state dirs from k8s config :)
    # grep mountPath /etc/kubernetes/manifests/ -r|sed 's:.* ::'|sort|uniq
    kubectl_config = "/root/.kube/config"
    cert_dir = '/etc/ssl/certs'
    # separate_state() moves directories around, don't want to confuse docker
    # and everything running within it. stopped_docker ensures we stop/start it
    dirs = ['/etc/kubernetes', cert_dir, '/var/lib/etcd',
            docker_lib_dir, docker_data_dir, '/var/lib/kubelet', '/usr/libexec/kubernetes/kubelet-plugins']
    dest = "/state"
    for srcdir in dirs:
        destdir = dest + srcdir
        have_state = os.path.exists(destdir)
        # if dest dir does not exist, there is no pre-existing state. Copy it
        # from source, but only if source isn't a symlink
        if not have_state:
            srcdir_is_dir = False
            run("mkdir -p " + destdir)
            try:
                mode = os.stat(srcdir)[ST_MODE]
                srcdir_is_dir = S_ISDIR(mode) and not S_ISLNK(mode)
            except OSError:
                pass
            if srcdir_is_dir:
                maybe_stop_docker(srcdir)
                # unlike mv this handles empty subdirectories
                run("tar -C {src} --one-file-system -c .| tar -C {destdir}/ -x".format(
                    src=srcdir, destdir=destdir))
        ensure_symlink(srcdir, destdir)
        if not have_state and srcdir == cert_dir:
            # if we didn't have certs in /state or pre-existing ones to copy.
            # Need to generate new ones
            run("/usr/sbin/update-ca-certificates -f")
    ensure_symlink(kubectl_config, "/etc/kubernetes/admin.conf", force=True)
    if stopped_docker:
        run("systemctl start docker")

def write_file(filename, body):
    with open(filename, 'w') as outfile:
        outfile.write(body)
    print "Wrote %d bytes to %s" % (len(body), filename)

def fix_resolv_conf():
    write_file("/etc/resolv.conf", """
nameserver 10.7.1.41
nameserver 10.7.32.31
search dev.purestorage.com purestorage.com
# puppetized base resolv.conf.d/tail options
options rotate timeout:2 attempts:2
domain dev.purestorage.com
""")

def main():
    fix_resolv_conf()
    separate_state()
    for interface, ip in CONFIG.iteritems():
        if not interface[0:4] == "data":
            continue
        run("ifconfig {interface} {ip} netmask 255.255.255.0 up".format(ip=ip, interface=interface))
    if os.path.exists("/etc/kubernetes/admin.conf"):
        sys.exit(0)
    #systemd does not set $HOME, this makes kubectl confused
    os.environ["HOME"] = "/root"
    run("kubeadm init --pod-network-cidr 10.244.0.0/16")
    # flannel + rbac permissions
    run("cd %s/k8s-vagrant && ./k8s_config.sh" % MY_DIR)
    run("cp {config} {dest}".format(config=CONFIG_FILE, dest=MY_DIR + "/k8s-provisioner/pure.json"))
    run("cd %s/k8s-provisioner && docker build -t pure-provisioner:local ." % MY_DIR)
    # install pure provisioner
    run("cd %s/k8s-provisioner && ./install_local.sh" % MY_DIR)

main()
