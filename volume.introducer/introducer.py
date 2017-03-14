import subprocess
import sys
import os.path
import json

def run(cmd):
    print cmd
    sys.stdout.flush()
    return subprocess.check_output(cmd, shell=True)

def from_file(json_file):
    root_dir = os.path.join(os.path.dirname(sys.argv[0]), "..")
    return json.loads(open(os.path.join(root_dir, json_file)).read())

def provision_database(mnt_dir, port):
    service = from_file("postgres-service.json")
    port_suffix = "-" + str(port)
    service['spec']['ports'][0]['nodePort'] = port
    service['spec']['ports'][0]['name'] += port_suffix
    service['spec']['selector']['role'] += port_suffix
    service['metadata']['name'] += port_suffix
    print(json.dumps(service,indent=2))

    rc = from_file("postgres-withvolume.json")
    


def add_volume(volume_path):
    stdout = run('sg_inq -p 0x83 ' + volume_path)
    volume_name = stdout.split(' ')[-1].strip()
    print volume_name
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
    run('mount %s %s' % (volume_path, mnt_dir))
    port = int(volume_name.split('-')[1])
    provision_database(mnt_dir, port)

def main():
    [volume] = sys.argv[1:]
    add_volume(volume)

main()
