# Get pods in all namespaces
def get_pods():
    import requests
    from kubernetes import client, config

    apiserver = "https://kubernetes.default.svc"
    serviceaccount="/var/run/secrets/kubernetes.io/serviceaccount"
    k8stoken = ""
    cacert = ""
    pods = []

    # Getting SA token
    with open(serviceaccount + "/token") as f:
        k8stoken = f.read()

    # Getting CA certificate
    with open(serviceaccount + "/ca.crt") as f:
        cacert = f.read()

    # Configuration for k8s client
    configuration = client.Configuration()
    configuration.api_key["authorization"] = k8stoken
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = apiserver
    configuration.ssl_ca_cert = serviceaccount + "/ca.crt"

    v1 = client.CoreV1Api(client.ApiClient(configuration))

    # Get all pods in all namespaces and return them
    print("Listing pods on all namespaces:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        pods.append(i.metadata.name)
    return pods