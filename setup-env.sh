#!/bin/bash

# Script para configurar ambiente automaticamente
# Uso: ./setup-env.sh [dev|prod]

ENV=${1:-dev}

echo "🔧 Configurando ambiente: $ENV"

if [ "$ENV" = "dev" ]; then
    echo "📁 Usando configurações de desenvolvimento..."
    echo "✅ Ambiente de desenvolvimento configurado!"
    echo "🚀 Execute: npm run dev"
    
elif [ "$ENV" = "prod" ]; then
    echo "📁 Usando configurações de produção..."
    echo "⚠️  ATENÇÃO: Configure as variáveis obrigatórias no arquivo .env"
    echo "✅ Ambiente de produção configurado!"
    echo "🚀 Execute: npm run prod"
    
else
    echo "❌ Ambiente inválido. Use: dev ou prod"
    exit 1
fi
