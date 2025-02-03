# Software/DataHarvester/src/validation/database_rules.py

from typing import Dict, Any
from .base_validator import BaseValidator
from domain.exceptions.domain_exceptions import ValidationError
from validation.rules.validation_rules import DATABASE_CONNECTION_RULES, DATABASE_RETRY_RULES

class DatabaseValidator(BaseValidator):
    def __init__(self):
        self.connection_fields = DATABASE_CONNECTION_RULES
        self.retry_fields = DATABASE_RETRY_RULES

    def validate(self, config: Dict[str, Any]) -> bool:
        """Validate database configuration."""
        try:
            # Validate top-level structure
            required_fields = {
                'connection': dict,
                'retry': dict,
                'collections': dict,
                'error_codes': dict
            }
            self._validate_required_fields(config, required_fields)

            # Validate nested structures
            self._validate_required_fields(config['connection'], self.connection_fields)
            self._validate_required_fields(config['retry'], self.retry_fields)

            # Validate collections structure
            for collection, settings in config['collections'].items():
                if not isinstance(settings.get('indexes', []), list):
                    raise ValidationError(
                        f"Collection {collection} indexes must be a list", 
                        "VAL006"
                    )

            return True
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Database validation failed: {str(e)}", "VAL007") 