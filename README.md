# Liquid Location Intelligence

API serverless para análise de localizações brasileiras com dados geográficos, econômicos e climáticos.

**Liquid Location Intelligence** é uma API serverless inteligente que fornece dados técnicos objetivos sobre localizações brasileiras, permitindo que clientes tirem suas próprias conclusões sobre investimentos imobiliários.

**Backend**: Python 3.12 + AWS Lambda + API Gateway + DynamoDB + JWT  
**Frontend**: React + Vite + Context API  
**Infra**: Serverless Framework + GitHub Actions CI/CD

## Arquitetura

```
 backend-liquid-inteligence/     # Backend Python
   ├── app/                        # Aplicação principal
   │   ├── controllers/            # Controllers
   │   ├── services/              # Lógica de negócio
   │   ├── repositories/          # Acesso a dados
   │   ├── external/              # Clientes de APIs externas
   │   ├── middleware/             # Middlewares
   │   └── utils/                 # Utilitários
   ├── tests/                     # Testes automatizados
   ├── .github/workflows/         # CI/CD Pipeline
   ├── serverless.yml             # Configuração Serverless
   └── requirements.txt           # Dependências Python
```

## APIs Integradas

- **ViaCEP**: Dados geográficos brasileiros
- **Banco Central**: SELIC + IPCA
- **OpenWeatherMap**: Clima + qualidade do ar

## Deploy

**Automático**: Push para `main` → GitHub Actions → AWS  
**Manual**: `serverless deploy`

## Endpoints

```bash
POST /api/auth/register    # Registro
POST /api/auth/login       # Login
POST /api/location/analyze # Análise (JWT required)
GET  /health              # Health check
```

## Exemplo de Uso

```bash
# Login
curl -X POST https://y8a1kr1ku9.execute-api.us-east-1.amazonaws.com/dev/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Análise
curl -X POST https://y8a1kr1ku9.execute-api.us-east-1.amazonaws.com/dev/api/location/analyze \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"location": "93230-600"}'
```

## Resposta da Análise

```json
{
  "success": true,
  "data": {
    "location": "93230-600",
    "geographic": {
      "cep": "93230-600",
      "street": "Avenida Juventino Machado",
      "city": "Sapucaia do Sul",
      "state": "RS",
      "coordinates": {"lat": -29.8275, "lng": -51.1464}
    },
    "economic": {
      "interest_rate": 8.5,
      "inflation": 4.2
    },
    "climate": {
      "temperature": 22,
      "humidity": 65,
      "air_quality": {"aqi": 2, "aqi_description": "Fair"}
    }
  }
}
```

## Desenvolvimento

```bash
# Backend
cd backend-liquid-inteligence
pip install -r requirements.txt
python -m pytest tests/unit/test_services/ -v

# Frontend  
cd frontend-liquid-inteligence
npm install
npm run dev
```

## Configuração

**Secrets GitHub Actions**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY` 
- `JWT_SECRET`
- `WEATHER_API_KEY`

