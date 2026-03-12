# clone

## Fonte
https://git-scm.com/docs/git-clone

## Explicação

Claro, vamos começar com o que é git clone?

1. O que é git clone?
`git clone` é um comando no Git que você usa para criar uma cópia de um repositório existente em outro lugar. Isso inclui todos os arquivos do projeto, todas as versões anteriores e histórico de commits.

2. Explicação simples
Imagine que você tem um projeto grande e complexo que está em um servidor remoto. Você quer trabalhar nesse projeto, mas não pode acessá-lo diretamente no seu computador. O comando `git clone` permite que você crie uma cópia deste repositório em seu próprio computador. Isso é como se você fizesse um backup do projeto para sua máquina local.

3. Exemplo prático
Suponha que você tem um repositório GitHub chamado `minhapasta` e deseja clonar esse repositório em seu computador. Você pode fazer isso digitando o seguinte comando no terminal:
```bash
git clone https://github.om/username/minhapasta.git
```
Esse comando criará uma nova pasta chamada `minhapasta` na sua localização atual, e dentro dessa pasta haverá todo o conteúdo do repositório remoto.

4. Quando usar
Você deve usar `git clone` sempre que quiser trabalhar em um projeto existente sem a necessidade de acesso direto ao servidor onde ele está hospedado. Isso pode ser uma cópia local para edição e testes, ou simplesmente para obter uma versão mais recente do projeto.

5. Observação importante
O `git clone` cria um link direto ao repositório remoto