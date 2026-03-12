# Regras de salvamento de explicações

## Regra inicial
O assistente não deve salvar toda resposta automaticamente.

## Quando salvar
Salvar somente quando o usuário pedir explicitamente.

## Exemplos de comando
- salvar explicação
- save: aws/alb-vs-nlb
- salvar na base

## Objetivo
Evitar poluir a base de conhecimento com respostas desnecessárias, repetidas ou temporárias.

## Fluxo desejado
1. Usuário faz uma pergunta
2. Assistente responde
3. Se o usuário quiser guardar, ele pede para salvar
4. A resposta vira um arquivo `.md` dentro da knowledge-base