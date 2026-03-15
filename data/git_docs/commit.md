# Git Commit

O comando `git commit` é um dos principais comandos do sistema Git, utilizado para registrar as alterações no histórico do repositório.

## Funcionamento

Após adicionar arquivos com o comando `git add`, você pode criar um "ponto" no histórico do seu projeto com a mensagem explicativa da alteração utilizando o comando `git commit`. Essa mensagem é chamada de mensagem de commit e deve ser escrita em inglês para facilitar a leitura por outras pessoas que trabalham no projeto.

## Exemplo

```bash
git add arquivo.txt
git commit -m "Adiciona arquivo inicial"
```

Neste exemplo, o comando `git add arquivo.txt` adicionou um arquivo chamado `arquivo.txt` ao próximo conjunto de alterações que serão commitadas. Em seguida, o comando `git commit -m "Adiciona arquivo inicial"` criou um ponto no histórico do projeto e registrou uma mensagem explicando a mudança feita: "Adiciona arquivo inicial".

## Casos de Uso

- **Registrar Mudanças no Código**: O comando `git commit` permite que você registre as alterações feitas em seu código. Isso ajuda a manter um histórico do progresso e permite que você volte para versões anteriores do seu código, caso necessário.
  
- **Criar Histórico de Desenvolvimento**: O comando `git commit` também é usado para criar um histórico de desenvolvimento do projeto. Cada commit registra uma mudança feita no código, permitindo que você veja o histórico completo das alterações feitas ao longo do tempo.
  
- **Permitir Rollback para Versões Anteriores**: Se algo der errado e você precisar voltar para uma versão anterior do seu código, o comando `git commit` permite que isso seja feito facilmente. Você pode escolher um ponto no histórico e "desfazer" tudo o que foi feito a partir desse ponto para retornar à versão anterior do seu código.

Por fim, é importante ressaltar que a documentação original não precisa de muitas melhorias em termos técnicos, mas sim na forma como ela é apresentada e organizada para facilitar a compreensão do leitor.
