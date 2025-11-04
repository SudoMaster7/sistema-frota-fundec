#!/bin/bash
# 🚀 SCRIPT PARA RODAR A APLICAÇÃO

# Navegar até a pasta do projeto
cd "$(dirname "$0")"

# Verificar se as dependências estão instaladas
echo "📌 Verificando dependências..."
python -m pip show flask > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Flask não está instalado. Instalando dependências..."
    pip install -r requirements.txt
fi

# Verificar se credentials.json existe
if [ ! -f "credentials.json" ]; then
    echo ""
    echo "⚠️  AVISO: Arquivo 'credentials.json' não encontrado!"
    echo ""
    echo "Para usar em DESENVOLVIMENTO:"
    echo "  1. Baixe credentials.json do Google Cloud Console"
    echo "  2. Coloque na pasta: $(pwd)/credentials.json"
    echo ""
    echo "Para PRODUÇÃO, configure:"
    echo "  export GOOGLE_CREDENTIALS_JSON='seu-json-aqui'"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Rodar a aplicação
echo ""
echo "🚀 Iniciando aplicação..."
echo "   Acesse: http://localhost:5000"
echo ""
python app.py
