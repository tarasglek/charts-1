import subprocess
import sys

def run(cmd):
    print cmd
    sys.stdout.flush()
    return subprocess.check_output(cmd, shell=True)

def add_volume(volume_path):
    stdout = run('sg_inq -p 0x83 ' + volume_path)
    volume_name = stdout.split(' ')[-1].strip()
    print volume_name
    mnt_dir = '/mnt/' + volume_name
    run('mkdir -p ' + mnt_dir)
    try:
        run('mkfs.xfs ' + volume_path)
    except:
        pass
    run('mount %s %s' % (volume_path, mnt_dir))

def main():
    [volume] = sys.argv[1:]
    add_volume(volume)

main()
