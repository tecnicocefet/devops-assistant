# LAB: Criando Diretórios com o Comando mkdir

## LAB BÁSICO
### Objetivo
Este laboratório tem como objetivo ensinar a criar diretórios no Linux usando o comando `mkdir`.

### Pré-requisitos
Um sistema operacional Linux instalado e configurado para uso.

### Cenário
Você está na sua área de trabalho e deseja criar um novo diretório chamado "novo_diretorio".

### Passos
1. Abra o terminal (CTRL + ALT + T).
2. Navegue até a pasta onde você deseja criar o novo diretório usando o comando `cd` seguido do caminho para essa pasta. Por exemplo, se você quiser criar um diretório na sua área de trabalho, use:
```bash
cd Desktop/
```
3. Digite e execute o comando a seguir para criar o novo diretório:
```bash
mkdir novo_diretorio
```
4. Pressione ENTER para criar o diretório.

### Desafio extra
Crie um novo diretório chamado "outro_diretorio" dentro do seu diretório atual.

### Resultado esperado
Você deve ver a nova pasta "novo_diretorio" aparecer na sua área de trabalho ou no local onde você navega.

## LAB INTERMEDIÁRIO
### Objetivo
Neste laboratório, o objetivo é ensinar a criar vários diretórios ao mesmo tempo usando o comando `mkdir` e opções de linha de comando.

### Pré-requisitos
O LAB BÁSICO concluído.

### Cenário
Você está na sua área de trabalho e deseja criar vários novos diretórios ao mesmo tempo.

### Passos
1. Abra o terminal (CTRL + ALT + T).
2. Navegue até a pasta onde você deseja criar os novo diretório usando o comando `cd` seguido do caminho para essa pasta. Por exemplo, se você quiser criar um diretório na sua área de trabalho, use:
```bash
cd Desktop/
```
3. Digite e execute o comando a seguir para criar vários novos diretórios ao mesmo tempo, separados por espaço:
```bash
mkdir dir1 dir2 dir3
```
4. Pressione ENTER para criar os diretórios.

### Desafio extra
Crie três novos diretórios chamados "dir4", "dir5" e "dir6" dentro do seu diretório atual.

### Resultado esperado
Você deve ver as novas pastas "dir1", "dir2", "dir3", "dir4", "dir5" e "dir6" aparecerem na sua área de trabalho ou no local onde você navega.

## LAB AVANÇADO
### Objetivo
Neste laboratório, o objetivo é ensinar a criar diretórios com permissões específicas usando o comando `mkdir` e opções de linha de comando.

### Pré-requisitos
O LAB INTERMEDIÁRIO concluído.

### Cenário
Você está na sua área de trabalho e deseja criar um novo diretório com permissões específicas.

### Passos
1. Abra o terminal (CTRL + ALT + T).
2. Navegue até a pasta onde você deseja criar os novo diretório usando o comando `cd` seguido do caminho para essa pasta. Por exemplo, se você quiser criar um diretório na sua área de trabalho, use:
```bash
cd Desktop/
```
3. Digite e execute o comando a seguir para criar um novo diretório com permissões específicas (por exemplo, leitura e execução para usuários):
```bash
mkdir -m 755 novo_diretorio2
```
4. Pressione ENTER para criar o diretório.

### Desafio extra
Crie um novo diretório chamado "novo_diretorio3" com permissões de leitura e execução para todos (755).

### Resultado esperado
Você deve ver a nova pasta "novo_diretorio2" e "novo_diretorio3" aparecerem na sua área de trabalho ou no local onde você navega, com as permissões corretas.

## Fonte
[mkdir](https://www.gnu.)org/software/coreutils/manual/html_node/mkdir-invocation.html#mkdir-invocation)