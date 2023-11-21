# Service Mesh [![wakatime](https://wakatime.com/badge/user/018bea20-dbbc-48e2-b101-5415903acf5a/project/018bf23f-423c-4bf1-b1d9-135ba7578aef.svg)](https://wakatime.com/@diegosneves/projects/otoebwtaou)
Service Mesh com Istio

---

## K3D:

Url: [*k3d*](https://k3d.io/)

1) link de instalação:

```shell
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

---



- Criando o cluster com 2 nodes para você acessar os nodes através da porta 8000.

```shell
k3d cluster create -p "8000:30000@loadbalancer" --agents 2
```
*Saida da tela:*

```shell
INFO[0000] portmapping '8000:30000' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] Prep: Network                                
INFO[0000] Created network 'k3d-k3s-default'            
INFO[0000] Created image volume k3d-k3s-default-images  
INFO[0000] Starting new tools node...                   
INFO[0001] Creating node 'k3d-k3s-default-server-0'     
INFO[0001] Pulling image 'ghcr.io/k3d-io/k3d-tools:5.6.0' 
INFO[0004] Starting Node 'k3d-k3s-default-tools'        
INFO[0004] Pulling image 'docker.io/rancher/k3s:v1.27.4-k3s1' 
INFO[0007] Creating node 'k3d-k3s-default-agent-0'      
INFO[0007] Creating node 'k3d-k3s-default-agent-1'      
INFO[0007] Creating LoadBalancer 'k3d-k3s-default-serverlb' 
INFO[0008] Pulling image 'ghcr.io/k3d-io/k3d-proxy:5.6.0' 
INFO[0019] Using the k3d-tools node to gather environment information 
INFO[0019] HostIP: using network gateway 172.20.0.1 address 
INFO[0019] Starting cluster 'k3s-default'               
INFO[0019] Starting servers...                          
INFO[0019] Starting Node 'k3d-k3s-default-server-0'     
INFO[0022] Starting agents...                           
INFO[0022] Starting Node 'k3d-k3s-default-agent-0'      
INFO[0022] Starting Node 'k3d-k3s-default-agent-1'      
INFO[0025] Starting helpers...                          
INFO[0025] Starting Node 'k3d-k3s-default-serverlb'     
INFO[0031] Injecting records for hostAliases (incl. host.k3d.internal) and for 4 network members into CoreDNS configmap... 
INFO[0033] Cluster 'k3s-default' created successfully!  
INFO[0033] You can now use it like this:                
kubectl cluster-info
```



- Verificando os nodes criados.

```shell
kubectl get nodes
```

*Saída da tela:*
```shell
NAME                       STATUS   ROLES                  AGE     VERSION
k3d-k3s-default-server-0   Ready    control-plane,master   8m32s   v1.27.4+k3s1
k3d-k3s-default-agent-0    Ready    <none>                 8m30s   v1.27.4+k3s1
k3d-k3s-default-agent-1    Ready    <none>                 8m30s   v1.27.4+k3s1
```

---

## Istio:

Url: [Istio](https://istio.io/)      |     Docs: [Istio Doc](https://istio.io/latest/docs/)



### instalação:

- Download:

  - ```shell
    curl -L https://istio.io/downloadIstio | sh -
    ```

- Adicione o cliente istioctl ao seu caminho (Linux):

  - ```shell
    export PATH=$PATH:~/istio-1.20.0/bin
    ```

  - ```shell
    source ~/.bashrc
    ```

- Após escolher o [perfil](https://istio.io/latest/docs/setup/getting-started/#install) execute o comando para instalação:

  - ```shell
    istioctl install -y
    ```
    - Exemplo de perfil `demo`:

      - ```shell
        istioctl install --set profile=demo -y
        ✔ Istio core installed
        ✔ Istiod installed
        ✔ Egress gateways installed
        ✔ Ingress gateways installed
        ✔ Installation complete
        ```

  
  
- Validar instalação pelo terminal:

  - ```shell
    kubectl get ns
    ```

    Ao usar o comando acima deve aparecer na lista o `istio-system` conforme exemplo abaixo:

    ```shell
    NAME              STATUS   AGE
    default           Active   4h51m
    kube-system       Active   4h51m
    kube-public       Active   4h51m
    kube-node-lease   Active   4h51m
    istio-system      Active   66m
    ```
    
    
    
  - Utilize o seguinte comando:

  - ```shell
    kubectl get pod -n istio-system
    ```

    ```shell
    NAME                                    READY   STATUS    RESTARTS   AGE
    istiod-7d4885fc54-rrhgq                 1/1     Running   0          69m
    istio-ingressgateway-56558c9fd7-hbhxk   1/1     Running   0          69m
    ```
    
    
    
  - Seus pods serão exibidos na tela. 

- Outras validações:

  - ```shell
    kubectl get svc
    ```

  deve ser exibido dados do service conforme exemplo abaixo:

  ```shell
  NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
  kubernetes   ClusterIP   10.43.0.1    <none>        443/TCP   4h59m
  ```

  - ```shell
    kubectl get svc -n istio-system
    ```
  
    ```text
    NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                      AGE
    istiod                 ClusterIP      10.43.33.239    <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP        78m
    istio-ingressgateway   LoadBalancer   10.43.236.123   <pending>     15021:32400/TCP,80:30279/TCP,443:31788/TCP   78m
    ```



---

## Sidecar Proxy

- Adicione um rótulo de namespace para instruir o Istio a injetar automaticamente proxies secundários quando você implantar seu aplicativo posteriormente:

```shell
kubectl label namespace default istio-injection=enabled
```

- Crie um `deployment` conforme exemplo abaixo:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
#  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      name: nginx
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            limits:
              memory: "128Mi"
              cpu: "500m"
          ports:
            - containerPort: 80
```

- Aplique o `deployment`:
```shell
kubectl apply -f src/github/k8s/deployment.yaml 
```

- Veja a saida com o comando abaixo:
```shell
kubectl get pod
```

---