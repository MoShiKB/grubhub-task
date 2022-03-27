def get_pods():
    import requests
    from kubernetes import client, config


    apiserver = "https://kubernetes.default.svc"
    serviceaccount="/var/run/secrets/kubernetes.io/serviceaccount"
    k8stoken = ""
    cacert = ""
    pods = []

    with open(serviceaccount + "/token") as f:
        k8stoken = f.read()

    with open(serviceaccount + "/ca.crt") as f:
        cacert = f.read()


    configuration = client.Configuration()
    configuration.api_key["authorization"] = k8stoken
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.host = apiserver
    configuration.ssl_ca_cert = serviceaccount + "/ca.crt"

    v1 = client.CoreV1Api(client.ApiClient(configuration))

    print("Listing pods on all namespaces:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        pods.append(i.metadata.name)
    return pods