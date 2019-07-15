import sys
import yaml
import time
import commands
def apply_vs(depname):
    with open("Deployment/istio-vs.yaml") as fp:
        virtuals = fp.read()
    virtuals = yaml.load(virtuals)
    virtuals["spec"]["http"][0]["route"][0] = {'destination': {'host': depname, 'port': {'number': 80}}}
    with open("vs_test.yaml","w+") as fp:
        fp.write(yaml.dump(virtuals))
    commands.getoutput("kubectl apply -n deployment -f vs_test.yaml")
prod_name = sys.argv[1]+"-phpredis"
fresh_name = sys.argv[2]+"-phpredis"

apply_vs(prod_name)
while True:
    op = commands.getoutput("kubectl get pods -n deployment | grep {0} | grep Running | wc -l".format(fresh_name))
    if int(op) == 1:
        break
    time.sleep(5)
apply_vs(fresh_name)
