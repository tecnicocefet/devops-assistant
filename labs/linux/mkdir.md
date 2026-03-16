## LAB BÁSICO
### Objetivo
Criar um novo diretório usando o comando `mkdir` básico.

### Pré-requisitos
Um ambiente Linux configurado e acessível.

### Cenário
Você está na sua máquina local e deseja criar um novo diretório chamado "novo_diretorio".

### Passos
1. Abra o terminal de comando.
2. Digite `mkdir novo_diretorio` e pressione Enter para criar o diretório.
3. Verifique se o diretório foi criado digitando `ls` e pressionando Enter. Você deve ver "novo_diretorio" na lista de arquivos/diretórios.

### Desafio extra
Experimente a opção `-v` para tornar o comando mais informativo, mostrando uma mensagem para cada diretório criado:
```bash
mkdir -v novo_diretorio
```

## LAB INTERMEDIÁRIO
### Objetivo
Criar um novo diretório com permissões específicas e verificar a criação do mesmo.

### Pré-requisitos
Um ambiente Linux configurado e acessível, bem como o conhecimento básico de permissões em sistemas Unix/Linux (modo 755).

### Cenário
Você está na sua máquina local e deseja criar um novo diretório chamado "minha_pasta" com as permissões de acesso 755.

### Passos
1. Abra o terminal de comando.
2. Digite `mkdir -m 755 minha_pasta` e pressione Enter para criar o diretório com as permissões desejadas.
3. Verifique se o diretório foi criado digitando `ls -l minha_pasta` e pressionando Enter. A saída deve mostrar os detalhes do arquivo, incluindo as permissões (nesse caso, 755).

### Desafio extra
Experimente a opção `-p` para criar diretórios pais necessários. Por exemplo:
```bash
mkdir -p pasta/subpasta/minha_pasta
```
Esse comando irá criar "pasta", "subpasta" e "minha_pasta" se eles ainda não existirem.

## LAB AVANÇADO
### Objetivo
Criar um novo diretório definindo o contexto de segurança SELinux para uma pasta específica.

### Pré-requisitos
Um ambiente Linux configurado e acessível, bem como conhecimento básico sobre SELinux e seus contextos.

### Cenário
Você está na sua máquina local e deseja criar um novo diretório chamado "minha_pasta" com o contexto de segurança definido para uma pasta específica (por exemplo, "system_u:object_r:default_t:s0").

### Passos
1. Abra o terminal de comando.
2. Digite `mkdir --context="system_u:object_r:default_t:s0" minha_pasta` e pressione Enter para criar o diretório definindo o contexto de segurança.
3. Verifique se o diretório foi criado digitando `ls -Z minha_pasta` e pressionando Enter. A saída deve mostrar os detalhes do arquivo, incluindo o contexto de segurança (nesse caso, "system_u:object_r:default_t:s0").

### Desafio extra
Experimente a opção `-v` para tornar o comando mais informativo, mostrando uma mensagem para cada diretório criado:
```bash
mkdir -v --context="system_u:object:default_t:s0" minha_pasta
```
Esse comando irá mostrar uma mensagem para cada pasta criada, indicando o contexto de segurança definido.

IMPORTANTE: O conhecimento básico sobre SELinux e seus contextos é necessário para este laboratório avançado. Caso você não saiba o que é um contexto de segurança, recomenda-se estudar esse tópico antes de prosseguir com este laboratório.