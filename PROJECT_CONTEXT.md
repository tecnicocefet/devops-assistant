Projeto

DevOps Assistant Local

Ferramenta educacional DevOps que roda 100% local, com:

análise de código DevOps

geração de labs práticos

leitura de documentação

leitura de man pages Linux

explicação com LLM

base de conhecimento local

interface CLI + Web

🧱 Stack principal

Python

FastAPI

Ollama

HTML + JS

Streaming de resposta

highlight.js

🧠 Arquitetura do projeto

Separação clara entre lógica e interface:

modules/   → lógica do sistema
cli/       → interface CLI
web/       → interface web

Ou seja:

modules
   ↓
CLI ou Web

Isso permite crescer o projeto facilmente.

📂 Estrutura atual
modules/
    code_analyzer/
        analyzer.py

    lab_generator/
        generator.py

    doc_reader/
        reader.py

    man_reader/
        reader.py

    official_docs/
        online_reader.py

cli/
    assistant_cli.py

web/
    routes/
        pages.py

    templates/
        pages/
            analyzer.html
            labs.html
            reader.html
            kb.html
            home.html
🧪 Funcionalidades já funcionando
1️⃣ Code Analyzer

Fluxo:

código
↓
detecção de tipo
↓
validador real
↓
se erro
    LLM explica
    LLM corrige

Validadores:

Bash

shellcheck

bash -n

shfmt

YAML

yamllint

Dockerfile

hadolint

Docker Compose

docker compose config

Terraform

terraform validate

terraform fmt -check

2️⃣ Labs Generator

Gera labs com estrutura:

# LAB

## LAB BÁSICO
## LAB INTERMEDIÁRIO
## LAB AVANÇADO

Pode:

gerar

salvar

listar

abrir

Diretório:

labs/
   linux/
   docker/
   terraform/

Streaming funcionando na web.

3️⃣ Documentation Reader

Página web:

/reader

Permite:

Doc local
git/commit
docker/run
terraform/init

Busca em:

data/*_docs/

Funções:

ler doc

melhorar doc com LLM

salvar doc

4️⃣ Man Page Reader

Permite:

mkdir
grep
tar

Fluxo:

man comando
↓
limpeza de formatação
↓
limite de tamanho
↓
LLM explica

Também pode salvar em:

data/linux_docs/
🌊 Streaming Web

Implementado com:

FastAPI StreamingResponse
+
fetch
+
ReadableStream

Fluxo:

FastAPI
StreamingResponse
↓
fetch()
↓
reader.read()
↓
append no chat-box

Streaming funciona em:

Analyzer

Labs

Reader (parcial)

🎨 Interface Web atual

Páginas:

/
Home

/analyzer
Analisar código

/labs
Gerar labs

/reader
Documentação + man page

/kb
Knowledge Base
⚠️ Pontos detectados durante teste
1️⃣ Melhorar doc não está fazendo streaming real

Motivo:

ollama.chat(..., stream=False)

Resultado:

CPU do modelo sobe

mas a resposta só aparece no final

2️⃣ Salvar doc não trata conflito de nome

Hoje:

arquivo.md
↓
salva direto

Não pergunta:

sobrescrever

salvar com outro nome

cancelar

3️⃣ Falta botão limpar tela

Outras páginas têm.

Reader ainda não tem.

4️⃣ Man pages podem vir em inglês

Modelo explica normalmente em português, mas ideal reforçar no prompt:

Explique em português do Brasil
🎯 Ordem de melhorias definida

Para evitar complexidade agora.

Etapa 1 (UX)

Resolver:

1️⃣ botão Limpar tela
2️⃣ salvar com opções:

já existe
↓
sobrescrever
salvar com novo nome
cancelar

Arquivos envolvidos:

reader.html
pages.py
doc_reader/reader.py
man_reader/reader.py
Etapa 2 (modelo)

Depois melhorar streaming real:

melhorar doc

explicar man page

Arquivos:

modules/doc_reader/reader.py
modules/man_reader/reader.py
web/routes/pages.py

Mudança principal:

stream=False
→
stream=True
🧩 Estado atual do projeto

Sistema funcional:

CLI funcionando

Web funcionando

Streaming funcionando

Analyzer funcionando

Labs funcionando

Reader funcionando

Doc + Man funcionando

Salvamento funcionando

Faltam apenas acabamentos finais da interface web.

🚀 Objetivo

Fechar DevOps Assistant v1.0

Interface web completa.

Depois disso o projeto fica pronto para evoluir para:

novos validadores

novos tipos de labs

cache de docs

plugins DevOps

📌 Como iniciar o próximo chat

Comece assim:

Continuar DevOps Assistant.

Reader já funciona, mas precisamos implementar:

1) botão limpar tela
2) salvar doc com tratamento de conflito
3) depois melhorar streaming real do modelo

Assim retomamos exatamente daqui.