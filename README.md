# DevOps Assistant

Assistente DevOps local executado via CLI, utilizando modelos LLM locais com Ollama.

O objetivo do projeto é fornecer uma ferramenta de estudo e consulta para tecnologias DevOps como Linux, Docker, Kubernetes, Terraform, Git e AWS.

## Funcionalidades

- Consulta de documentação local
- Consulta de man pages do sistema
- Consulta de documentação oficial online
- Base de conhecimento local (knowledge-base)
- Explicações geradas por modelos locais
- Melhoria automática de documentação
- Geração futura de labs práticos

## Comandos disponíveis

doc:tecnologia/assunto  
Consulta documentação local

webdoc:tecnologia/assunto  
Consulta documentação oficial online

man:comando  
Explica man pages do Linux

melhorar doc:assunto  
Melhora documentação local

verificar doc:assunto  
Audita conteúdo da knowledge-base

salvar base:tecnologia/assunto  
Salva explicação na base de conhecimento

## Estrutura do projeto

devops-assistant
├── cli
├── modules
├── data
├── knowledge-base
├── labs
├── commands
├── docs
├── models

## Tecnologias

- Python
- Ollama
- DeepSeek Coder
- Qwen Coder

## Roadmap

- Interface web
- Geração automática de labs
- Análise de código DevOps
- Busca semântica em documentação
