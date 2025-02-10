# Software/DataHarvester/services/data_ingestion/validation/validators/base_validator.py   

from typing import Dict, Any
from abc import ABC, abstractmethod
from domain.exceptions.domain_exceptions import ValidationError

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> bool:
        """Validate configuration."""
        pass

    def _validate_required_fields(self, config: Dict[str, Any], required_fields: Dict[str, type]) -> bool:
        """Validate required fields and their types."""
        try:
            for field, expected_type in required_fields.items():
                if field not in config:
                    raise ValidationError(f"Missing required field: {field}", "VAL001")
                if not isinstance(config[field], expected_type):
                    raise ValidationError(
                        f"Field {field} must be of type {expected_type.__name__}", 
                        "VAL002"
                    )
            return True
        except Exception as e:
            raise ValidationError(f"Validation failed: {str(e)}", "VAL003") 