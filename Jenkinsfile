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
	/*stage('DeployMonitoring') {
        OLD_BUILD_NUMBER = sh(script: "helm ls | grep prometheus | awk '{print\$1}'",returnStdout: true).trim()
        echo "${OLD_BUILD_NUMBER}"
        sh "kubectl create ns monitoring || true"
        sh "kubectl label namespace monitoring istio-injection=enabled || true"
	
	def backend = sh(returnStatus: true, script: "helm ls | grep -q prometheus")
        if(backend != 0){
            sh "helm install --namespace monitoring --name prometheus stable/prometheus-node-exporter --set prometheus.replicaCount=1"
        }
        POD_NAME = sh(script: "kubectl get pods --namespace monitoring -l \"app=prometheus-node-exporter,release=prometheus\" -o jsonpath=\"{.items[0].metadata.name}\"",returnStdout: true).trim()
        echo "Visit http://127.0.0.1:8080 to use prometheus-node-exporter"
	echo "${POD_NAME}"	
	SERVICE_NAME = sh(script: "kubectl get svc --namespace monitoring | awk '{print\$2}'",returnStdout: true).trim()
	sh "kubectl patch svc $SERVICE_NAME --namespace monitoring -p '{\"spec\": {\"type\": \"LoadBalancer\"}}'"
	//SERVICE_IP = sh(script: "kubectl get svc $POD_NAME --namespace monitoring --output jsonpath='{.status.loadBalancer.ingress[0].ip}'",returnStdout: true).trim()
	sh "kubectl get svc --namespace monitoring "
	sh "kubectl --namespace monitoring port-forward $POD_NAME 9000"	
	}*/
       
}
