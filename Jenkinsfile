node {
    def redisslave
    stage('Clone repository') {
	checkout scm
    }

    stage('DeployApplication') {
        // Ensure Namespace Deployment is labeled for istio injection
        def status = sh(returnStatus: true, script: "helm ls | grep -q guestbook")
        OLD_BUILD_NUMBER = sh(script: "helm ls | grep guestbook | awk '{print\$1}'",returnStdout: true).trim()
        echo "${OLD_BUILD_NUMBER}"
        sh "kubectl create ns deployment || true"
        sh "kubectl label namespace deployment istio-injection=enabled || true"
        sh "kubectl create -n deployment -f Deployment/istio-gateway.yaml || true"
        
        //Ensure Backend is deployed
        def backend = sh(returnStatus: true, script: "helm ls | grep -q redisbackend")
        if(backend != 0){
            sh "helm install --namespace deployment --name redisbackend rediscluster  --set redisSlave.replicaCount=1"
        }
        
    }
	stage('DeployMonitoring') {
        OLD_BUILD_NUMBER = sh(script: "helm ls | grep prometheus | awk '{print\$1}'",returnStdout: true).trim()
        echo "${OLD_BUILD_NUMBER}"
        sh "kubectl create ns monitoring || true"
        sh "kubectl label namespace monitoring istio-injection=enabled || true"
	
	def backend = sh(returnStatus: true, script: "helm ls | grep -q prometheus")
        if(backend != 0){
            sh "helm install --namespace monitoring --name prometheus stable/prometheus-node-exporter --set prometheus.replicaCount=1"
        }
        POD_NAME= sh(script: "kubectl get pods --namespace monitoring -l \"app=prometheus-node-exporter,release=prometheus\" -o jsonpath=\"{.items[0].metadata.name}\")
        echo "Visit http://127.0.0.1:8080 to use prometheus-node-exporter"
	echo "${POD_NAME}"
	sh "kubectl --namespace monitoring port-forward \$POD_NAME 9100:90"
	sh "kubectl get svc --namespace monitoring "
	}
       
}
