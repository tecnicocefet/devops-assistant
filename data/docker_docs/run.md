# Comando docker run

O comando `docker run` é usado para criar e iniciar um container a partir de uma imagem Docker. Essencialmente, ele baixa a imagem (se necessário) e inicia um container baseado nela.

## Exemplo básico:

```bash
docker run nginx
```

Esse comando iniciará um container com o servidor Nginx.

## Exemplo com porta:

```bash
docker run -p 8080:80 nginx
```

Nesse caso, o Nginx estará disponível em `http://localhost:8080`. A opção `-p 8080:80` é um mapeamento de porta entre a sua máquina e o container, permitindo que você acesse o serviço web do Nginx através da porta 8080 em seu computador.

## Casos de uso:

1. **Executar aplicações isoladas**: O comando `docker run` permite que você execute várias instâncias de um mesmo aplicativo, cada uma delas sendo executada em seu próprio container. Isso é muito útil para evitar conflitos entre versões do software e para gerenciar ambientes de desenvolvimento e produção separados.

2. **Testar imagens Docker**: Você pode usar o comando `docker run` para testar rapidamente uma nova imagem Docker em um ambiente isolado. Isso é especialmente útil quando você está desenvolvendo sua própria imagem Docker e precisa garantir que ela funciona corretamente antes de publicá-la para o registro público ou privado.

3. **Rodar serviços rapidamente**: Com o comando `docker run`, você pode iniciar um container a partir de uma imagem Docker em segundos, sem precisar escrever comandos complexos para baixar e configurar uma imagem. Isso é muito útil para tarefas rápidas como iniciar um servidor web simples ou executar um aplicativo de linha de comando.
