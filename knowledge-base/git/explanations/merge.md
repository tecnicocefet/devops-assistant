# merge

## Fonte
https://git-scm.com/docs/git-merge

## Explicação

Bem vindo a um guia amigável e didático sobre o comando `git merge` do Git, que é fundamental para muitos desenvolvedores de software.

## O que é git merge?

O `git merge` é um dos comandos mais utilizados no Git. Ele permite que você integre as alterações feitas em duas ou mais ramificações (branches) do seu repositório. Isso é útil quando você tem tarefas a serem concluídas em diferentes partes do projeto e precisa integrar essas alterações em um só lugar.

## Explicação simples

Imagine que você está trabalhando numa equipe de desenvolvimento, onde cada membro da equipe tem uma ramificação separada do seu repositório (branch). Quando um membro conclui suas alterações e os testa localmente, ele cria uma nova versão do código.

O comando `git merge` permite que você integre essas novas versões de volta ao seu branch principal (geralmente o 'master' ou 'main'). Isso é feito integrando as alterações dos outros branches em um só lugar.

## Exemplo prático

Suponha que você tenha dois branches: `feature-a` e `feature-b`. Você pode fazer merge dessas duas ramificações usando o seguinte comando no terminal:

```bash
git checkout master  # Muda para o branch principal
git merge feature-a  # Faz merge da branch 'feature-a' no branch atual (master)
git merge feature-b  # Faz merge da branch 'feature-b' no branch atual (master)
```

## Quando usar

Normalmente, você usaria o `git merge` quando deseja integrar as alterações feitas em um branch separado ao seu principal. Isso é útil para manter o histórico de commits organizado e evitar conflitos de mesclagem.

## Observação importante

O `git merge` pode resultar em conflitos se as alterações nos dois branches que você está tentando mesclar alterarem a mesma linha no mesmo arquivo. Nesses casos, você terá de resolver manualmente os conflitos antes de conseguir fazer o merge.

Essas explicações foram feitas com base na documentação oficial do Git e podem não abranger todas as opções disponíveis para `git merge`, mas elas devem ajudá-lo a entender o que é e como usar esse poderoso comando no seu dia a dia como desenvolvedor.