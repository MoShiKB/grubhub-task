# Grubhub App
Grubhub App deploys applications with a few endpoints with different purposes
1. /pods - getting pods to name in all namespaces
2. /me - getting the IP address of the container
3. /metrics - getting metrics of client requests
4. /health - health check for the application

## Getting Started
These instructions will guide you on how to run and access the application.

### Prerequisites
Docker - containerization platform, allow packaging applications into containers, required to build our application.

Helm - tool to manage Kubernetes applications, allows easy definition, installation, and upgrade k8s applications.

Jenkins - CICD tool to build and push our docker image.

### Docker Stage
The first step is to build and push our application.

To build our app image, run these commands:

    docker build ./docker -f ./docker/Dockerfile -t moshikb/grubhub:latest

then, we can run our application using:

    docker run -p 5000:5000 moshikb/grubhub:latest

In order to access and run our REST API endpoint, enter http://localhost:5000/<endpoint here>

And the last step is to save our image remotely and push it to a registry:

    docker push moshikb/grubhub:latest

### Helm Chart:
In order to install our application on Kubernetes, we will install a helm chart, run that command: 

    helm install -n default grubhub ./grubhub

which installs:
1. Deployment - with readiness & liveness probe - checks /healthcheck
2. Service - to expose our application
3. Ingress - creates a reverse proxy endpoint to our application
4. HPA - allow scaling of the application
5. Configmap - contains environment variables for our application
6. ServiceAccount - k8s user for services, allow the pods to have permissions in the cluster
7. Role + RoleBinding - Defining the permissions for the ServiceAccount

### Jenkins Pipeline:
Pipeline to build and push our Dockerfile.

First, it clones the application repository from GitHub,
and then build the image using the docker plugin and push it with tags of:
    1. build number
    2. latest
and finishing with cleaning the built image from our agent.
