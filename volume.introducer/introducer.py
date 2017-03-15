#!/usr/bin/python
import subprocess
import sys
import os.path
import json
import tempfile
import re
import glob
import time

my_path = os.path.abspath(sys.argv[0])

class KubernetesException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(KubernetesException, self).__init__(message)


def run(cmd):
    print cmd
    sys.stdout.flush()
    return subprocess.check_output(cmd, shell=True)

def from_file(json_file):
    root_dir = os.path.join(os.path.dirname(my_path), "..")
    return json.loads(open(os.path.join(root_dir, json_file)).read())

def kubernetes_create(obj):
    obj_str = json.dumps(obj, indent=2)
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(obj_str)
    f.close()
    # print obj_str
    try:
        run("kubectl create -f " + f.name)
    except subprocess.CalledProcessError as e:
        raise KubernetesException(e.message)
    finally:
        os.remove(f.name)

def provision_database(mnt_dir, port):
    service = from_file("postgres-service.json")
    port_suffix = "-" + str(port)
    service['spec']['ports'][0]['nodePort'] = port
    service['spec']['ports'][0]['name'] += port_suffix
    service['spec']['selector']['role'] += port_suffix
    service['metadata']['name'] += port_suffix
    kubernetes_create(service)

    rc = from_file("postgres-withvolume.json")
    rc['spec']['template']['spec']['containers'][0]['name'] += port_suffix
    rc['spec']['template']['spec']['volumes'][0]['hostPath']['path'] = mnt_dir
    rc['spec']['template']['metadata']['labels']['role'] += port_suffix
    rc['spec']['selector']['role'] += port_suffix
    rc['metadata']['name'] += port_suffix
    kubernetes_create(rc)

def add_volume(volume_path):
    stdout = run('sg_inq -p 0x83 ' + volume_path)
    volume_name = stdout.split(' ')[-1].strip()
    db_volume_match = re.search(r'db-\d+$', volume_name)
    if not db_volume_match:
        print "(%s, %s) is not a db volume, skipping" % (volume_path, volume_name)
        return

    mnt_dir = '/mnt/' + volume_name
    run('mkdir -p ' + mnt_dir)
    try:
        run('umount %s' % (volume_path))
    except:
        pass
    try:
        run('mkfs.xfs ' + volume_path)
    except:
        pass
    run('mount -o nouuid %s %s' % (volume_path, mnt_dir))
    port = int(volume_name.split('-')[1])
    try:
        provision_database(mnt_dir, port)
    except KubernetesException as e:
        print "Failed to start K8S RS for (%s, %s): %s" % (volume_path, volume_name, str(e))

def scan_volumes():
    tried_before = set()
    while True:
        for volume in glob.glob("/dev/sd[a-z]*"):
            # skip partions
            c = volume[-1]
            if not volume in tried_before and c >= 'a' and c <= 'z':
                tried_before.add(volume)
                yield volume
        for sys_scan in glob.glob("/sys/class/scsi_host/*/scan"):
            with open(sys_scan, 'w') as outfile:
                outfile.write("- - -\n")
        time.sleep(1)

# tell systemd to start me on boot
def install_me():
    unit_def = """
[Unit]
Description=DB creation service

[Service]
ExecStart=%s

[Install]
WantedBy=multi-user.target""" % my_path
    unit_path = '/etc/systemd/system/introducer.service'
    with open(unit_path, 'w') as outfile:
        outfile.write(unit_def)
    run("systemctl enable %s" % os.path.basename(unit_path))

def main():
    if sys.argv[-1] == "--install":
        install_me()
    for volume in scan_volumes():
        add_volume(volume)

main()
