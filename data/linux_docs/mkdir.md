## O que o comando faz
O `mkdir` é um utilitário de linha de comando do Linux usado para criar diretórios. Quando executado, ele cria novos diretórios no sistema de arquivos. Se os diretórios já existirem, o `mkdir` não faz nada e retorna um código de erro.

## Sintaxe básica
A sintaxe básica do comando é: 
```bash
mkdir [opções] diretório1 [diretório2 ...]
```

## Principais opções
Algumas das principais opções incluem:
- `-m, --mode=MODE`: Define o modo de acesso dos arquivos criados no diretório.
- `-p, --parents`: Não retorna um erro se os diretórios já existirem. Em vez disso, ele cria qualquer diretório pai necessário com seus modos inalterados por qualquer opção -m.
- `-v, --verbose`: Imprime uma mensagem para cada diretório criado.
- `-Z, --context[=CTX]`: Define o contexto de segurança SELinux ou SMACK dos novos diretórios para os valores padrão do tipo, ou se CTX for especificado, define o contexto como CTX.

## Exemplos práticos
Crie um novo diretório chamado "novo_diretorio" na pasta atual:
```bash
mkdir novo_diretorio
```

Crie uma nova pasta com permissão de acesso especificada (por exemplo, modo 755):
```bash
mkdir -m 755 minha_pasta
```

Crie um novo diretório e seus pais:
```bash
mkdir -p pasta/subpasta/subsubpasta
```
Este comando criará `pasta`, `subpasta` e `subsubpasta` se eles ainda não existirem.

Crie um novo diretório definindo o contexto de segurança SELinux para "system_u:object_r:default_t:s0":
```bash
mkdir --context="system_u:object_r:default_t:s0" minha_pasta
```
Este comando criará `minha_pasta` e definirá o contexto de segurança para esse diretório.