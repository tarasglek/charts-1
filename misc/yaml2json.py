import sys, yaml, json
json.dump(yaml.load(sys.stdin), sys.stdout, indent=2)