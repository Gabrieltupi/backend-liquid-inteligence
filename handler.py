import json
import logging
from datetime import datetime
from typing import Dict, Any
from app.main import create_app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = create_app()

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        print("[HANDLER] Iniciando processamento da requisição")
        print(f"[HANDLER] Event recebido: {json.dumps(event)}")
        
        logger.info(f"Received event: {json.dumps(event)}")
        
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '{}')
        query_params = event.get('queryStringParameters', {}) or {}
        
        print(f"[HANDLER] Método: {http_method}, Path: {path}")
        print(f"[HANDLER] Headers: {headers}")
        print(f"[HANDLER] Body: {body}")
        
        request_context = {
            'method': http_method,
            'path': path,
            'headers': headers,
            'body': body,
            'query_params': query_params,
            'event': event,
            'context': context
        }
        
        print(f"[HANDLER] Request context criado: {request_context}")
        
        print("[HANDLER] Chamando app.process_request")
        response = app.process_request(request_context)
        print(f"[HANDLER] Resposta gerada: {response}")
        
        logger.info(f"Response: {json.dumps(response)}")
        
        return response
        
    except Exception as e:
        print(f"[HANDLER] ERRO CAPTURADO: {str(e)}")
        print(f"[HANDLER] Tipo do erro: {type(e)}")
        import traceback
        print(f"[HANDLER] Traceback: {traceback.format_exc()}")
        
        logger.error(f"Error processing request: {str(e)}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error_code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'timestamp': str(datetime.now())
            })
        }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    return handler(event, context)
