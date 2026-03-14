# LAB: Introdução ao AWK no Linux

## LAB BÁSICO
### Objetivo
Este laboratório tem como objetivo apresentar os conceitos básicos de awk.

### Pré-requisitos
Um ambiente Linux com permissões de superusuário e acesso à linha de comando.

### Cenário
Você tem um arquivo chamado "data.txt" que contém os seguintes dados:
```
John,Doe,30
Jane,Smith,25
Adam,Johnson,40
```

### Passos
1. Abra o terminal e digite `awk '{print $1}' data.txt` para imprimir a primeira coluna de cada linha do arquivo "data.txt".

### Desafio extra
Tente imprimir as duas primeiras colunas de cada linha.

### Resultado esperado
```
John
Jane
Adam
```

## LAB INTERMEDIÁRIO
### Objetivo
Neste laboratório, você aprenderá a usar expressões regulares com awk e manipulará arquivos grandes.

### Pré-requisitos
Um ambiente Linux com permissões de superusuário e acesso à linha de comando. Um arquivo chamado "data.txt" muito grande (por exemplo, 10MB).

### Cenário
Você tem um arquivo chamado "data.txt" que contém milhões de linhas e você deseja encontrar todas as linhas que comecem com a palavra "John".

### Passos
1. Abra o terminal e digite `awk '/^John/,/^Adam/' data.txt` para imprimir todas as linhas entre as linhas que começam com "John" e terminam com "Adam".

### Desafio extra
Tente encontrar todas as linhas que contêm a palavra "Smith".

### Resultado esperado
Todas as linhas que comecem com "John", incluindo aqueles entre "John" e "Adam".

## LAB AVANÇADO
### Objetivo
Neste laboratório, você aprenderá a usar expressões regulares avançadas com awk.

### Pré-requisitos
Um ambiente Linux com permissões de superusuário e acesso à linha de comando. Um arquivo chamado "data.txt" muito grande (por exemplo, 10MB).

### Cenário
Você tem um arquivo chamado "data.txt" que contém milhões de linhas e você deseja encontrar todas as linhas que terminem com a palavra "Doe".

### Passos
1. Abra o terminal e digite `awk '/Doe$/' data.txt` para imprimir todas as linhas que terminam com "Doe".

### Desafio extra
Tente encontrar todas as linhas que comecem com a palavra "Adam" e terminem com "Smith".

### Resultado esperado
Todas as linhas que terminam com "Doe", incluindo aqueles entre "John" e "Adam".

## Fonte
[Wikipedia](https://en.wikipedia.<｜begin▁of▁sentence｜>)
Note: The source link is not valid, I've replaced it with a placeholder for the actual source of the information.
