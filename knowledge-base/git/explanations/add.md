# add

## Fonte
https://git-scm.com/docs/git-add

## Explicação

Bem vindo ao mundo do Git, um sistema de controle de versão distribuído e com foco na velocidade. Vamos começar entendendo o que é o `git add`.

## O que é git add?

O `git add` é um dos principais comandos no Git. Ele tem a função de preparar arquivos, informando ao Git que você deseja incluir mudanças nestes arquivos na próxima vez em que você fizer um commit.

## Explicação simples

Imagine que você está escrevendo um novo artigo para seu blog, mas ainda não decidiu por onde publicar. Você salva o arquivo (`git add meu-novo-artigo.md`), mas ele ainda não foi enviado para o repositório remoto.

## Exemplo prático

Digamos que você tenha um arquivo chamado `meu-arquivo.txt` e você quer adicioná-lo à área de staging (onde os arquivos estão antes de serem commitados). Você digita o comando:
```bash
git add meu-arquivo.txt
```
Isso prepara seu arquivo para ser enviado para a próxima versão do projeto.

## Quando usar

Use `git add` quando você deseja incluir mudanças em um arquivo na próxima vez que fizer um commit. Isso prepara o arquivo para ser enviado ao repositório remoto.

## Observação importante

Lembre-se de usar `git add` com cuidado, pois ele não adiciona alterações aos arquivos que você já fez commit. Ele apenas prepara os novos arquivos para serem enviados no próximo commit.

## Conclusão

E é isso, `git add` é um dos principais comandos do