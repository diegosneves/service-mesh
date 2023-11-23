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
```textmate
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

  ```shell
  curl -L https://istio.io/downloadIstio | sh -
  ```

- Adicione o cliente istioctl ao seu caminho (Linux):

  ```shell
  export PATH=$PATH:~/istio-1.20.0/bin
  ```

  ```shell
  source ~/.bashrc
  ```

- Após escolher o [perfil](https://istio.io/latest/docs/setup/getting-started/#install)(ou deixe em branco para _default_) execute o comando para instalação:

  ```shell
  istioctl install -y
  ```
  - Exemplo de perfil `demo`:

    ```textmate
    istioctl install --set profile=demo -y
    ✔ Istio core installed
    ✔ Istiod installed
    ✔ Egress gateways installed
    ✔ Ingress gateways installed
    ✔ Installation complete
    ```

  
  
- Validar instalação pelo terminal:

  ```shell
  kubectl get ns
  ```

    Ao usar o comando acima deve aparecer na lista o `istio-system` conforme exemplo abaixo:

    ```textmate
    NAME              STATUS   AGE
    default           Active   4h51m
    kube-system       Active   4h51m
    kube-public       Active   4h51m
    kube-node-lease   Active   4h51m
    istio-system      Active   66m
    ```
    
    
  - Utilize o seguinte comando:

    ```shell
    kubectl get pod -n istio-system
    ```

    ```textmate
    NAME                                    READY   STATUS    RESTARTS   AGE
    istiod-7d4885fc54-rrhgq                 1/1     Running   0          69m
    istio-ingressgateway-56558c9fd7-hbhxk   1/1     Running   0          69m
    ```


- Seus pods serão exibidos na tela. 

- Outras validações:

  ```shell
  kubectl get svc
  ```

  deve ser exibido dados do service conforme exemplo abaixo:

  ```textmate
  NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
  kubernetes   ClusterIP   10.43.0.1    <none>        443/TCP   4h59m
  ```

  ```shell
  kubectl get svc -n istio-system
  ```
  
  ```textmate
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

## Configurando Addons:

- [Istio Integration](https://istio.io/latest/docs/ops/integrations/) possi tambem infos para configurar o [cert-manager](https://istio.io/latest/docs/ops/integrations/certmanager/)

- Para adicionar alguns addons para telemetria, basta encontrar na propria [doc do Istio](https://istio.io/latest/docs/setup/getting-started/#dashboard) o link para [Istio Integration](https://istio.io/latest/docs/ops/integrations/).
  - [Kiali](https://istio.io/latest/docs/ops/integrations/kiali/)
  ```shell
  kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
  ```
  - [Grafana](https://istio.io/latest/docs/ops/integrations/grafana/)
  ```shell
  kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
  ```
  - [Prometheus](https://istio.io/latest/docs/ops/integrations/prometheus/)
  ```shell
  kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
  ```
  - [Jaeger](https://istio.io/latest/docs/ops/integrations/jaeger/)
  ```shell
  kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
  ```
para o exemplo desse projeto foi utilizado esses quatros addons.

```shell
kubectl get pod -n istio-system
```

```textmate
NAME                                    READY   STATUS    RESTARTS        AGE
istiod-7d4885fc54-rrhgq                 1/1     Running   1 (7h34m ago)   19h
istio-ingressgateway-56558c9fd7-hbhxk   1/1     Running   1 (7h34m ago)   19h
kiali-cc67f8648-wbp8k                   1/1     Running   0               16m
grafana-5f9b8c6c5d-dqxcn                1/1     Running   0               16m
prometheus-5d5d6d6fc-txhrm              2/2     Running   0               15m
jaeger-db6bdfcb4-jjrbn                  1/1     Running   0               15m
```

```shell
kubectl get svc -n istio-system
```

```text
NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                          AGE
istiod                 ClusterIP      10.43.33.239    <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP            19h
istio-ingressgateway   LoadBalancer   10.43.236.123   <pending>     15021:32400/TCP,80:30279/TCP,443:31788/TCP       19h
kiali                  ClusterIP      10.43.91.134    <none>        20001/TCP,9090/TCP                               100s
grafana                ClusterIP      10.43.9.55      <none>        3000/TCP                                         76s
prometheus             ClusterIP      10.43.139.253   <none>        9090/TCP                                         53s
tracing                ClusterIP      10.43.62.51     <none>        80/TCP,16685/TCP                                 37s
zipkin                 ClusterIP      10.43.7.76      <none>        9411/TCP                                         37s
jaeger-collector       ClusterIP      10.43.65.194    <none>        14268/TCP,14250/TCP,9411/TCP,4317/TCP,4318/TCP   37s
```

---

## Obervabilidade:

### - [Kiali](https://istio.io/latest/docs/tasks/observability/kiali/):

- Para abrir a interface do Kiali, execute o seguinte comando em seu ambiente Kubernetes:
  ```shell
  istioctl dashboard kiali
  ```
![kiali](https://istio.io/latest/docs/tasks/observability/kiali/kiali-graph.png)

---

## Gerenciamento de tráfico (_[doc](https://istio.io/latest/docs/concepts/traffic-management/)_):

comando para auxiliar nas requests:

```shell
while true;do curl http://localhost:8000; echo; sleep 0.5; done;
```
Depois basta abrir o [Kiali](#--kiali) e verificar o trafico.

### [Fortio](https://istio.io/latest/docs/tasks/traffic-management/circuit-breaking/#adding-a-client):
```shell
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/httpbin/sample-client/fortio-deploy.yaml
```

Comando para teste de stress:

```shell
kubectl exec fortio-deploy-5669d4866b-76wss -c fortio -- fortio load -c 2 -qps 0 -t 200s -loglevel Warning http://nginx-service:8000
```

> Para facilitar é possivel pegar o nome do pod do fortio para atraves de um export:
> 
>```shell
>export FORTIO_POD=$(kubectl get pods -l app=fortio -o 'jsonpath={.items[0].metadata.name}')
>```
>isso evita ter que usar algo tipo `fortio-deploy-5669d4866b-76wss` para executar o comando.
>```shell
>kubectl exec "$FORTIO_POD" -c fortio -- fortio load -c 2 -qps 0 -t 200s -loglevel Warning http://nginx-service:8000
>```

---

## Consistent Hash:

Na config abaixo definimos que o `trafficPolicy` tera seu `loadBalancer` como um `consistentHash` para 'guardar' o header name(`httpHeaderName : "x-user"`).
Isso enviara o usuario sempre para o mesmo pod.

exemplo:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: nginx-vs
  labels:
    app: nginx-vs
spec:
  hosts:
    - nginx-service
  http:
    - route:
        - destination:
            host: nginx-service
            subset: all

---

apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: nginx-dr
  labels:
    app: nginx-dr
spec:
  host: nginx-service
  trafficPolicy:
    loadBalancer:
      consistentHash:
        httpHeaderName: "x-user" # Esse 'x-user' pode ser qualquer valor;
  subsets:
    - name: all
      labels:
        app: nginx
```


---

## Docker
Vamor criar uma imagem Nginx para utlizar nesse projeto:

### NGINX:
As imagens Nginx para esse projeto terão apenas diferencas no `body` do html.

- index.html
  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minha Página</title>
  </head>
  <body>
    <h1>Diego A</h1>
  </body>
  </html>
  ```
  esse html iremos alterar o `body` onde um dos valores será `Diego A` e o outro `Diego B`. Isso servirá para realizar alguns testes.
- Dockerfile
  ```yaml
  FROM nginx:latest
  LABEL authors="diegoneves"

  COPY index.html /user/share/nginx/html/

  EXPOSE 80
  ```
  Vamos criar duas versões.

- Faca o login:
  ```shell
  docker login
  ```
- build:
  > Altere os valores necessarios `docker build -t seu-usuario-dockerhub/nome-imagem:tag .`
  ```shell
  docker build -t diegoneves/nginx-sn:latest .
  ```
  Após buildar, faca o `push` para o [DockerHub](https://hub.docker.com/) utilizando o seguinte comando:
  ```shell
  docker push diegoneves/nginx-sn:latest
  ```
Agora altere o valor do `body` no index para `Diego B` e repita o processo alterando a tag `latest` para `b`.


---