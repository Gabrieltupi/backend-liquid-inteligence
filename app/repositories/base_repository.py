
import boto3
import os
from typing import Dict, Any, Optional

class BaseRepository:
    
    def __init__(self):
        self.dynamodb = None
        self.table_name = None
        self._init_dynamodb()
    
    def _init_dynamodb(self):
        """Inicializa conexão com DynamoDB"""
        try:
            
            self.dynamodb = boto3.resource('dynamodb')
            
            
        except Exception as e:
            self.dynamodb = None
    
    def _get_table(self):
        """Retorna a tabela DynamoDB"""
        if not self.dynamodb or not self.table_name:
            return None
        
        try:
            table = self.dynamodb.Table(self.table_name)
            return table
        except Exception as e:
            return None
