# LAB: Utilizando o grep no Linux

## LAB BÁSICO
### Objetivo
Neste laboratório básico, você aprenderá a usar o comando `grep` para procurar padrões em arquivos de texto.

### Pré-requisitos
Você deve ter um sistema operacional Linux instalado e familiarizado com a interface de linha de comando (CLI). Você também precisa ter o `grep` instalado no seu sistema.

### Cenário
Você tem um arquivo chamado `texto.txt` que contém os seguintes textos:
```
Olá, meu nome é João e tenho 20 anos.
Eu estudo na UTFPR no curso de Ciência da Computação.
Estou aprendendo a usar o grep no Linux.
```
### Passos
1. Abra um terminal.
2. Use o comando `grep` para procurar a palavra "Linux" no arquivo `texto.txt`:
   ```
   grep 'Linux' texto.txt
   ```
3. Você deve ver a seguinte saída:
   ```
   Estou aprendendo a usar o grep no Linux.
   ```
### Desafio extra
Experimente procurar por outras palavras ou padrões no arquivo `texto.txt`. Por exemplo, você pode procurar pela palavra "UTFPR" para encontrar todas as linhas que contêm essa palavra.

### Resultado esperado
Você deve conseguir usar o comando `grep` para localizar padrões específicos em arquivos de texto no Linux.

## LAB INTERMEDIÁRIO
### Objetivo
Neste laboratório intermediário, você aprenderá a usar expressões regulares com o `grep` para procurar padrões mais complexos em arquivos de texto.

### Pré-requisitos
Você deve ter um sistema operacional Linux instalado e familiarizado com a interface de linha de comando (CLI). Você também precisa ter o `grep` instalado no seu sistema.

### Cenário
Você tem um arquivo chamado `texto2.txt` que contém os seguintes textos:
```
192.168.0.1 - - [30/Jul/2022:15:45:30 +0300] "GET /index.html HTTP/1.1" 200 277 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
192.168.0.2 - - [30/Jul/2022:15:45:31 +0300] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0<｜begin▁of▁sentence｜>0.4389.82 Safari/537.36"
```
### Passos
1. Abra um terminal.
2. Use o comando `grep` para procurar as linhas que contêm "Windows NT 6.1" no arquivo `texto2.txt`:
   ```
   grep 'Windows NT 6.1' texto2.txt
   ```
3. Você deve ver a seguinte saída:
   ```
   192.168.0.1 - - [30/Jul/2022:15:45:30 +0300] "GET /index.html HTTP/1.1" 200 277 "-" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
   ```
### Desafio extra
Experimente usar expressões regulares com o `grep` para encontrar linhas que contêm um IP específico, como "192.168.0.1".

### Resultado esperado
Você deve conseguir usar o comando `grep` junto com expressões regulares para localizar padrões mais complexos em arquivos de texto no Linux.

## LAB AVANÇADO
### Objetivo
Neste laboratório avançado, você aprenderá a usar o `grep` com opções avançadas para procurar padrões específicos em arquivos de texto.

### Pré-requisitos
Você deve ter um sistema operacional Linux instalado e familiarizado com a interface de linha de comando (CLI). Você também precisa ter o `grep` instalado no seu sistema.

### Cenário
Você tem um arquivo chamado `texto3.txt` que contém os seguintes textos:
```
Olá, meu nome é João e tenho 20 anos.
Eu estudo na UTFPR no curso de Ciência da Computação.
Estou aprendendo a usar o grep no Linux.
```
### Passos
1. Abra um terminal.
2. Use o comando `grep` com a opção `-i` para procurar uma palavra que não diferencia maiúsculas e minúsculas:
   ```
   grep -i 'linux' texto3.txt
   ```
3. Você deve ver a seguinte saída:
   ```
   Estou aprendendo a usar o grep no Linux.
   ```
### Desafio extra
Experimente usar outra opção do `grep`, como `-v` para inverter a busca e procurar linhas que não contenham um padrão específico. Por exemplo, você pode usar o comando `grep -v 'UTFPR' texto3.txt` para encontrar todas as linhas que não contêm "UTFPR".

### Resultado esperado
Você deve conseguir usar opções avançadas do comando `grep` para localizar padrões específicos em arquivos de texto no Linux.

## Fonte
Este laboratório foi baseado na documentação oficial do GNU grep (https://www.gnu.<｜begin▁of▁sentence｜>org/software/grep/manual/html_node/index.html#SEC_Contents) e em outras fontes de conhecimento aberto.
