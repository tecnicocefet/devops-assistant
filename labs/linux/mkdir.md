# LAB: Criando Diretórios com o comando mkdir

## Objetivo

Este laboratório tem como objetivo ensinar o uso do comando `mkdir` no Linux para criar diretórios (pastas) no sistema de arquivos, incluindo a criação de múltiplos diretórios, diretórios aninhados e o uso de algumas opções úteis do comando.

---

## Pré-requisitos

Para realizar este laboratório você precisa de:

- Um sistema Linux ou uma máquina virtual Linux
- Acesso ao terminal
- Permissão para criar arquivos e diretórios no seu diretório home

---

## Cenário

Você está no seu diretório home (`~`) e deseja organizar uma estrutura de diretórios para seus estudos e projetos.

---

## Passos

### 1. Abra o terminal

Abra o terminal do seu sistema Linux.

---

### 2. Navegue até o diretório home

Digite:

cd ~

Para confirmar onde você está, execute:

pwd

---

### 3. Criar um diretório simples

Crie um diretório chamado **Projetos**:

mkdir Projetos

Verifique se ele foi criado:

ls

---

### 4. Criar vários diretórios ao mesmo tempo

Agora crie dois diretórios de uma vez:

mkdir Pasta1 Pasta2

Verifique novamente:

ls

Você deverá ver:

Projetos  
Pasta1  
Pasta2  

---

### 5. Criar outro diretório no diretório atual

Crie um diretório chamado **Documentos**:

mkdir Documentos

Verifique:

ls

---

### 6. Criar diretórios aninhados

Agora vamos criar uma estrutura de diretórios usando a opção `-p`.

Execute:

mkdir -p Estudos/Linux/Comandos

Isso criará automaticamente toda a estrutura:

Estudos  
└── Linux  
  └── Comandos  

Para visualizar a estrutura criada você pode usar:

tree

(se o comando `tree` estiver instalado)

---

## Explorando opções do mkdir

### 7. Usar a opção `-v` (verbose)

A opção `-v` mostra mensagens informando os diretórios criados.

mkdir -v TesteVerbose

Você verá algo semelhante a:

mkdir: created directory 'TesteVerbose'

---

### 8. Usar a opção `-m` (permissões)

A opção `-m` permite definir permissões no momento da criação.

mkdir -m 755 DiretorioPermissoes

Verifique as permissões:

ls -l

---

### 9. Usar a opção `-Z` (contexto de segurança SELinux)

Em sistemas que utilizam **SELinux**, a opção `-Z` define o contexto de segurança.

mkdir -Z DiretorioSELinux

> Esta opção funciona corretamente apenas se o SELinux estiver ativo.

---

### 10. Usar a opção `-i` (modo interativo)

A opção `-i` pede confirmação antes da criação.

mkdir -i DiretorioInterativo

O sistema perguntará se você realmente deseja criar o diretório.

---

## Desafio extra

Crie a seguinte estrutura de diretórios com **um único comando**:

devops  
└── docker  
  └── volumes  
    └── logs  

### Dica

Utilize a opção `-p`.

## Resumo

- Como criar estruturas de diretórios aninhadas
- Como usar opções importantes como `-p`, `-v`, `-m`, `-Z` e `-i`

Você também terá criado uma pequena estrutura de diretórios para praticar organização de arquivos no Linux.
