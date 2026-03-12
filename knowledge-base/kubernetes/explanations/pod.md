# pod

## Fonte
https://kubernetes.io/docs/concepts/workloads/pods/

## Explicação

1. O que é um Pod?
Pods são os menores componentes implementáveis de computação que você pode criar e gerenciar no Kubernetes. 

2. Explicação simples
Imagine um Pod como sendo um grupo de um ou mais contêineres, com recursos de rede e armazenamento compartilhados, e uma especificação para rodar os contêineres. Um Pod's conteúdo é sempre colocado juntos e agendados em um contexto compartilhado, e roda em um mesmo ambiente. Um Pod modela uma aplicação específica "host" lógico: ele contém um ou mais contêineres de aplicativos que estão muito próximos uns dos outros.

3. Exemplo prático
Aqui está um exemplo de um Pod que consiste em um contêiner rodando a imagem nginx:1.14.2
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```
Para criar o Pod mostrado acima, execute o seguinte comando: `kubectl apply -f https://k8s.io/examples/pods/simple-pod.yaml`

4. Quando usar
Pods são usados principalmente em dois casos principais no Kubernetes: Pods que rodam um único contêiner e Pods que rodam vários contêineres que precisam trabalhar juntos.

5. Observação importante
Um Pod é geralmente criado não diretamente, mas através de recursos de carga de trabalho como Deployments ou Jobs. Além disso, se sues contêineres precisarem rastrear estados, considere o uso do StatefulSet.

Lembrando que um Pod é uma entidade relativamente temporária e despreparada, como um host para seus contêineres rodarem. O nome de um Pod deve ser um valor válido para subdomínio DNS, mas isso pode produzir resultados inesperados para o nome do host do Pod. Para melhor compatibilidade, o nome deve seguir as regras mais restritivas para um subdomínio.