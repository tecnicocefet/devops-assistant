# clone

## Fonte
https://git-scm.com/docs/git-clone

## Explicação

Claro, vamos começar com o que é `git clone`?

1. O que é git-clone?
   
   É um comando do Git usado para criar uma cópia de um repositório existente em outro local no seu sistema. Quando você clona um repositório, você obterá uma cópia completa dos arquivos e histórico de alteraçõao do projeto.

2. Explicação simples:
   
   Imagine que você está trabalhando em um projeto com outras pessoas, e cada uma delas tem seu próprio repositório no GitHub. Para obter o código de um colega, você pode usar `git clone` para criar uma cópia local do seu amigo's repositório.

3. Exemplo prático:
   
   Suponha que você esteja usando GitHub e tem o projeto "minha-aplicacao" armazenado nele. Você pode clonar esse repositório para seu computador executando o seguinte comando no terminal:
   ```bash
   git clone https://github.com/meu-usuario/minha-aplicacao.git
   ```
   Isso criará uma nova pasta chamada "minha-aplicacao" na sua localização atual, e dentro dela terá todos os arquivos do projeto.

4. Quando usar:
   
   Você deve usar `git clone` quando você deseja obter uma cópia completa de um repositório para trabalhar localmente em cima dele sem a necessidade de se conectar à internet.

5. Observação importante:
   
   É importante lembrar que `git clone` não é apenas uma cópia rasa dos arquivos, mas também os históricos de alterações e branches do repositório remoto. Isso significa que você pode fazer commits locais sem se preocupar com sincronizar as alterações com o repositório original.
   
Espero ter ajudado a entender melhor o `git clone` e como ele funciona no Git. Se você tiver mais dúvidas, não hesite em perguntar.