# Software/DataHarvester/src/validation/scraping_rules.py

from typing import Dict, Any
from validation.validators.base_validator import BaseValidator
from validation.rules.validation_rules import SCRAPING_RULES

class ScrapingValidator(BaseValidator):
    def validate(self, config: Dict[str, Any]) -> bool:
        required_fields = {
            'scraping': dict,
            'youtube_api': dict,
            'error_patterns': list
        }
        
        self._validate_required_fields(config, required_fields)
        self._validate_required_fields(config['scraping'], SCRAPING_RULES)
        
        return True 