#!/usr/bin/env bash
set -euo pipefail

arquivo_origem="arquivo.txt"
diretorio_destino="pasta"

if [[ ! -f "$arquivo_origem" ]]; then
    echo "Erro: arquivo '$arquivo_origem' não encontrado."
    exit 1
fi

mkdir -p "$diretorio_destino"
cp "$arquivo_origem" "$diretorio_destino/"

echo "Arquivo copiado com sucesso para '$diretorio_destino/'."