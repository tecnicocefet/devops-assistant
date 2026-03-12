# Application Load Balancer vs Network Load Balancer

## Pergunta
Qual a diferença entre Application Load Balancer (ALB) e Network Load Balancer (NLB) na AWS?

## Tecnologia
AWS

## Fonte
Documentação oficial AWS

## Data
2026-03-11

## Explicação

O Application Load Balancer (ALB) e o Network Load Balancer (NLB) são dois tipos de load balancers do AWS Elastic Load Balancing.

A principal diferença entre eles está na camada do modelo OSI em que operam.

### Application Load Balancer (ALB)

O ALB opera na **Camada 7 (Application Layer)**.

Ele entende protocolos HTTP e HTTPS e consegue tomar decisões baseadas em informações da requisição.

Características principais:

- Roteamento baseado em **URL path**
- Roteamento baseado em **host**
- Integração com **microservices**
- Suporte a **containers e Kubernetes**
- Ideal para **APIs e aplicações web**

Exemplo de roteamento:

/api → serviço API  
/images → serviço de imagens

### Network Load Balancer (NLB)

O NLB opera na **Camada 4 (Transport Layer)**.

Ele trabalha diretamente com conexões TCP e UDP e não interpreta o conteúdo da requisição.

Características principais:

- **Altíssima performance**
- **Baixíssima latência**
- Suporte a milhões de conexões simultâneas
- Preserva o **IP original do cliente**

É ideal para:

- serviços TCP
- bancos de dados
- aplicações que exigem alta performance de rede

## Resumo rápido

ALB → Layer 7 → HTTP/HTTPS → aplicações web e APIs  
NLB → Layer 4 → TCP/UDP → alta performance de rede

## Tags

aws, alb, nlb, load-balancer, networking