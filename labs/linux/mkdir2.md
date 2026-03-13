# LAB: mkdir - Criação de diretórios no Linux

## LAB BÁSICO
### Objetivo
Este laboratório tem como objetivo ensinar a criar um único diretório e entender sua sintaxe básica.

### Pré-requisitos
Um ambiente Linux configurado para este laboratório.

### Cenário
Você está na sua máquina local, no terminal do Linux. Você deseja criar um diretório chamado "Projetos".

### Passos
1. Digite o seguinte comando: `mkdir Projetos`
2. Pressione Enter para executar o comando.

Você deve ver uma mensagem indicando que o diretório foi criado com sucesso.

### Desafio extra
Crie um novo diretório chamado "Documentos" dentro do atual.

## LAB INTERMEDIÁRIO
### Objetivo
Neste laboratório, você aprenderá a criar vários diretórios de uma vez e entenderá como usar o parâmetro -p para criar pastas intermediárias.

### Pré-requisitos
O LAB BÁSICO concluído com sucesso.

### Cenário
Você está na raiz do sistema de arquivos e deseja criar duas pastas: "Pasta1" e "Pasta2".

### Passos
1. Digite o seguinte comando: `mkdir Pasta1 Pasta2`
2. Pressione Enter para executar o comando.

Você deve ver mensagens indicando que as pastas foram criadas com sucesso.

### Desafio extra
Crie uma estrutura de diretório aninhada, como "Pasta1/Pasta2". Use o parâmetro -p para isso.

## LAB AVANÇADO
### Objetivo
Neste laboratório avançado, você aprenderá a usar opções comuns do mkdir e entenderá como elas podem ser úteis em situações específicas.

### Pré-requisitos
O LAB INTERMEDIÁRIO concluído com sucesso.

### Cenário
Você está na raiz do sistema de arquivos e deseja criar uma pasta chamada "Documentos". Você também quer que essa pasta tenha permissões especiais para o usuário, grupo e outros.

### Passos
1. Digite o seguinte comando: `mkdir -m 750 Documentos`
2. Pressione Enter para executar o comando.

Você deve ver uma mensagem indicando que a pasta foi criada com sucesso. Use o comando `ls -ld Documentos` para confirmar as permissões da pasta.

### Desafio extra
Crie um novo diretório chamado "Pasta3" e use a opção -p para criar uma subpasta dentro dele, como "Pasta3/Subpasta". Verifique se as permissões da pasta são corretas.

### Resultado esperado
Você terá um novo diretório chamado "Documentos" na raiz do sistema com as permissões especificadas e uma estrutura de pastas aninhadas conforme o desafio extra.