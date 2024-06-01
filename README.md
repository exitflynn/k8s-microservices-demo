# K8s Microservices Demo

This project is designed as a playground for learning and building cloud projects using Kubernetes and microservices. It provides the code for basic APIs written in Python, with Docker images hosted on [Dockerhub](https://hub.docker.com/u/exitflynn). The project includes Horizontal Pod Autoscaling, which can be tested using stress tests written with [Locust](https://locust.io/). The deployment can be done on local environments like Minikube or cloud platforms like Azure AKS or GCP GKE, AWS EKS, etc.

## Setup Instructions

### Prerequisites

- Docker
- Kubernetes (Minikube or a cloud provider like Azure Kubernetes Service)
- kubectl
- Locust (for stress testing)

### Docker Images

The Docker images for the services are available on Dockerhub:
- [exitflynn/barcode](https://hub.docker.com/r/exitflynn/barcode)
- [exitflynn/catalog](https://hub.docker.com/r/exitflynn/catalog)
- [exitflynn/cdn](https://hub.docker.com/r/exitflynn/cdn)

### Running on Minikube

1. **Start Minikube:**
   ```sh
   minikube start
   ```

2. **Deploy MySQL:**
   ```sh
   kubectl apply -f manifests/mysql-storageclass.yaml
   kubectl apply -f manifests/mysql-pv.yaml
   kubectl apply -f manifests/mysql-pvc.yaml
   kubectl apply -f manifests/mysql-deployment.yaml
   kubectl apply -f manifests/mysql-service.yaml
   ```

3. **Deploy Barcode Service:**
   ```sh
   kubectl apply -f manifests/barcode-deployment.yaml
   ```

4. **Deploy Catalog Service:**
   ```sh
   kubectl apply -f manifests/catalog-deployment.yaml
   ```

5. **Deploy CDN Service:**
   ```sh
   kubectl apply -f manifests/cdn-deployment.yaml
   kubectl apply -f manifests/cdn-service.yaml
   ```

6. **Access Services:**
   Use `minikube service <service-name>` to access the services. Example:
   ```sh
   minikube service cdn-service
   ```

### Running on Azure Kubernetes Service (AKS)

1. **Create an AKS cluster:**
   ```sh
   az aks create -g <resource-group> -n <cluster-name> --node-count 1 --enable-addons monitoring --generate-ssh-keys
   ```

2. **Get AKS credentials:**
   ```sh
   az aks get-credentials -g <resource-group> -n <cluster-name>
   ```

3. **Deploy MySQL:**
   ```sh
   kubectl apply -f manifests/mysql-storageclass.yaml
   kubectl apply -f manifests/mysql-pv.yaml
   kubectl apply -f manifests/mysql-pvc.yaml
   kubectl apply -f manifests/mysql-deployment.yaml
   kubectl apply -f manifests/mysql-service.yaml
   ```

4. **Deploy Barcode, Catalog, and CDN Services:**
   ```sh
   kubectl apply -f manifests/barcode-deployment.yaml
   kubectl apply -f manifests/catalog-deployment.yaml
   kubectl apply -f manifests/cdn-deployment.yaml
   kubectl apply -f manifests/cdn-service.yaml
   ```

5. **Access Services:**
   Use `kubectl get services` to get the external IP addresses for the services.

### Horizontal Pod Autoscaling

1. **Enable HPA:**
   Ensure that your cluster has the metrics server installed. You can use the following command to deploy the metrics server on Minikube:
   ```sh
   minikube addons enable metrics-server
   ```

2. **Apply HPA configuration:**
   ```sh
   kubectl apply -f manifests/traffic-generator.yaml
   ```

3. **Stress Test using Locust:**
   - Install Locust:
     ```sh
     pip install locust
     ```
   - Run Locust tests:
     ```sh
     locust -f catalog/stress_test.py
     ```

There's plenty of room for production level improvementls (I originally made this for a Uni project), contributions in any form are welcome.
