Comando: docker run

O que faz:
Cria e executa um container a partir de uma imagem Docker.

Explicação simples:
O comando docker run baixa a imagem (se necessário) e inicia um
container baseado nela.

Exemplo:

docker run nginx

Isso inicia um container com o servidor Nginx.

Exemplo com porta:

docker run -p 8080:80 nginx

Agora o Nginx estará disponível em:
http://localhost:8080

Casos de uso:
- executar aplicações isoladas
- testar imagens Docker
- rodar serviços rapidamente
