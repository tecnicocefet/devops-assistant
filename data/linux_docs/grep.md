man:grep
## O que o comando faz
O `grep` é um utilitário de linha de comando usado para procurar padrões em arquivos ou entrada da linha de comando. Ele pode ser usado para encontrar textos específicos dentro dos arquivos e imprimir as linhas que correspondem a esses padrões.

## Sintaxe básica
A sintaxe básica do `grep` é:
```bash
grep 'padrao' arquivo1 arquivo2 ...
```
Onde "padrao" é o que você está procurando e os arquivos são onde você quer buscar esse padrão. Se nenhum arquivo for especificado, `grep` lerá do stdin (entrada padrão).

## Principais opções
Algumas das principais opções que podemos usar com o `grep` são:
- `-i` ou `--ignore-case`: Ignora diferenças entre maiúsculas e minúsculas.
- `-v` ou `--invert-match`: Inverte a seleção, imprimindo apenas as linhas que não correspondem ao padrão.
- `-c` ou `--count`: Não imprime nada além do contador de linhas que corresponderam.
- `-E` ou `--extended-regexp`: Interpreta o padrão como expressões regulares estendidas (EREs).
- `-F` ou `--fixed-strings`: Interpreta o padrão como strings fixas, não sendo interpretado como regex.

## Exemplos práticos
Por exemplo, para procurar a palavra "erro" em todos os arquivos .txt do diretório atual e imprimir apenas as linhas que contêm essa palavra:
```bash
grep 'erro' *.txt
```
Para encontrar todas as linhas no arquivo `meu_arquivo.txt` que não contenham a palavra "erro":
```bash
grep -v 'erro' meu_arquivo.txt
```
E para contar quantas linhas no arquivo `outro_arquivo.txt` contêm a palavra "erro":
```bash
grep -c 'erro' outro_arquivo.txt
```
Este é um resumo básico do comando `grep`, mas ele tem muitas opções e recursos para tornar sua busca mais eficiente e específica.
