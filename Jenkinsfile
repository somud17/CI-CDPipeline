node {
    def redisslave
    stage('Clone repository') {
	checkout scm
    }

    //stage('Build image') {
      //  frontend = docker.build("somud17/phpredis","./php-redis")
        //backend = docker.build("somud17/redisslave","./redis-slave")
    //}

    //stage('Push image') {
      //  docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
        //    frontend.push("${env.BUILD_NUMBER}")
          //  frontend.push("latest")
            //backend.push("${env.BUILD_NUMBER}")
            //backend.push("latest")
       // }
   //  }
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
        
        sh "helm install guest-book --name guestbook-${env.BUILD_NUMBER} --namespace deployment --set phpRedis.replicaCount=1  --set phpRedis.image.repository=kartiksharma522/phpredis --set phpRedis.image.tag=${env.BUILD_NUMBER} "
       // if( status == 0 ){
            //Canary Deployment
            //sh "python2 canary.py ${OLD_BUILD_NUMBER} guestbook-${env.BUILD_NUMBER} 10"

            //BlueGreen Deployment
         //   sh "python2 bluegreen.py ${OLD_BUILD_NUMBER} guestbook-${env.BUILD_NUMBER}"

           // sh "helm delete --purge ${OLD_BUILD_NUMBER} || true"
        //} else {
          //  sh "python2 first.py guestbook-${env.BUILD_NUMBER}"
       // }
    }
	stage('DeployMonitoring') {
        sh "helm get stable/prometheus-node-exporter"
        OLD_BUILD_NUMBER = sh(script: "helm ls | grep prometheus | awk '{print\$1}'",returnStdout: true).trim()
        echo "${OLD_BUILD_NUMBER}"
        sh "kubectl create ns monitoring || true"
        sh "kubectl label namespace monitoring istio-injection=enabled || true"
        sh "helm install --namespace monitoring --name prometheus --set prometheus.replicaCount=1"
	sh "kubectl expose monitoring prometheus --type=NodePort"
	sh "kubectl get svc --namespace monitoring"
       
}
