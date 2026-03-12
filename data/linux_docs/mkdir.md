# mkdir

## O que é

O mkdir é um comando no sistema operacional Unix/Linux que cria diretórios (pastas) em seu sistema de arquivos.

## Sintaxe

mkdir nome_do_diretorio

Essa é a sintaxe básica do comando mkdir para criar um único diretório.

## Exemplos

### Criar um diretório

mkdir Projetos

Essa linha de comando irá criar uma pasta no seu sistema chamada Projetos.

### Criar vários diretórios ao mesmo tempo

mkdir Pasta1 Pasta2

Esse comando cria duas pastas ao mesmo tempo:

- Pasta1
- Pasta2

### Criar um diretório dentro do diretório atual

mkdir Documentos

Cria uma pasta chamada Documentos dentro do diretório atual.

### Criar diretórios recursivamente

mkdir -p Pasta1/Pasta2

O parâmetro -p diz ao sistema para criar pastas intermediárias também, caso elas ainda não existam.

Por exemplo, se Pasta1 não existir, o sistema irá criá-la automaticamente antes de criar Pasta2.

## Opções comuns

| opção | descrição |
| --- | --- |
| -p | cria diretórios intermediários automaticamente |
| -v | mostra os diretórios criados |
| -m | define permissões do diretório |
| -Z | define contexto de segurança |
| -i | pede confirmação antes de criar |

1. `-p` cria diretórios intermediários automaticamente

Porém, o `mkdir` também tem outras opções:

1. `-v` ou `--verbose`: Esta opção faz com que o comando mostre mensagens detalhadas sobre o que está a fazer. Por exemplo, se criar um novo diretório, ele irá mostrar uma mensagem indicando isso e o nome do novo diretório.

1. `-m` ou `--mode`: Esta opção permite definir permissões para os novos arquivos criados. Por exemplo, `mkdir -m 755 dirname` irá criar um novo diretório chamado "dirname" com as permissões de leitura e execução para o proprietário, leitura para os membros do grupo e nenhuma permissão para outros.

1. `-Z`: Esta opção permite definir contextos de segurança para novos diretórios. Por exemplo, `mkdir -Z public_rw_t dirname` irá criar um novo diretório chamado "dirname" com o contexto de segurança "public_rw_t".

1. `-d`: Esta opção permite a criação apenas de diretórios, sem fazer nada caso já existam. Por exemplo, `mkdir -p dir1/dir2 && touch dir1/dir2/file` irá criar "dir1" e "dir2", mesmo que eles já existam.

1. `-i`: Esta opção pede uma confirmação antes de criar novos diretórios, caso eles ainda não existam.

## Observações

O mkdir também pode ser usado para criar estruturas completas de diretórios.  
A opção -p é muito útil quando você precisa criar várias pastas aninhadas de uma só vez.
