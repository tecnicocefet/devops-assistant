# O que o comando faz
O `grep` (global regular expression print) é um utilitário de linha de comando usado para procurar padrões em arquivos ou entrada da linha de comando. Ele pode ser usado para encontrar textos específicos dentro dos arquivos e imprimir as linhas que correspondem a esses padrões.

## Explicação simples
O `grep` é um utilitário muito útil para procurar por texto em arquivos. Você pode usá-lo para encontrar palavras específicas, expressões regulares ou padrões de caracteres dentro dos seus arquivos de texto.

## Exemplo prático
Por exemplo, se você quiser procurar a palavra "erro" em todos os arquivos .txt do seu diretório atual:
```bash
grep 'erro' *.txt
```
Isso irá imprimir todas as linhas que contém a palavra "erro". Se você quiser inverter essa busca e encontrar apenas as linhas onde não há a palavra "erro", você pode usar o comando:
```bash
grep -v 'erro' meu_arquivo.txt
```
E se você quiser contar quantas linhas no arquivo `outro_arquivo.txt` contém a palavra "erro", pode usar o comando:
```bash
grep -c 'erro' outro_arquivo.txt
```
## Casos de uso
O `grep` é usado em muitas situações, principalmente quando você precisa encontrar e trabalhar com padrões específicos dentro dos seus arquivos de texto ou código fonte. Ele pode ser usado para procurar erros no seu código, encontrar strings específicas em arquivos grandes, entre outras coisas.

Além disso, o `grep` tem muitas opções que podem tornar sua busca mais eficiente e específica, como a opção -i para ignorar maiúsculas e minúsculas, ou a opção -v para inverter a seleção.
