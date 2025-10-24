from typing import Dict, Any
from app.services.location_service import LocationService
from app.services.validation_service import ValidationService
from app.utils.formatters import ResponseFormatter
from app.utils.exceptions import ValidationError, ExternalServiceError

class LocationController:
    
    def __init__(self):
        self.location_service = LocationService()
        self.validation_service = ValidationService()
        self.response_formatter = ResponseFormatter()
    
    def analyze_location(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        print("[LOCATION_CONTROLLER] Iniciando análise de localização")
        print(f"[LOCATION_CONTROLLER] Request context: {request_context}")
        
        validated_data = self.validation_service.validate_location_request(
            request_context.get('body', '{}')
        )
        print(f"[LOCATION_CONTROLLER] Dados validados: {validated_data}")
        
        print(f"[LOCATION_CONTROLLER] Analisando localização: {validated_data['location']}")
        analysis_data = self.location_service.analyze_location(
            validated_data['location']
        )
        print(f"[LOCATION_CONTROLLER] Análise concluída: {analysis_data}")
        
        return self.response_formatter.success_response(
            data=analysis_data,
            message="Location analysis completed successfully"
        )
