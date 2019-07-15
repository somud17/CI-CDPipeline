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
canary_name = sys.argv[2]+"-phpredis"
rate = sys.argv[3]

apply_vs(prod_name)
with open("Deployment/istio-canary.yaml") as fp:
	canary = fp.read()
canary = yaml.load(canary)
rate = int(rate)
i = 0
while True:
    op = commands.getoutput("kubectl get pods -n deployment | grep {0} | grep Running | wc -l".format(canary_name))
    if int(op) == 1:
        break
    time.sleep(5)
while(True):
    i = i + rate
    i = min(i,100)
    canary["spec"]["http"][0]["route"][0] = {'destination': {'host': prod_name, 'port': {'number': 80}}, 'weight': 100-i}
    canary["spec"]["http"][0]["route"][1] = {'destination': {'host': canary_name, 'port': {'number': 80}}, 'weight': i}
    with open("canary_test.yaml","w+") as fp:
        fp.write(yaml.dump(canary))
    commands.getoutput("kubectl apply -n deployment -f canary_test.yaml")
    print("Deployment rolled --> ",i,"%")
    time.sleep(10)
    if i==100:
        break
apply_vs(canary_name)

