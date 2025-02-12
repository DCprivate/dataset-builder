# Software/DataHarvester/services/scraper_service/validation/validators/youtube_validator.py

from typing import Dict, Any, List
from validation.validators.base_validator import BaseValidator
from validation.rules.validation_rules import SCRAPING_RULES
import re

class YouTubeValidator:
    """Centralized YouTube-related validation."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate YouTube URL format."""
        patterns = [
            r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
            r'^https?://(?:www\.)?youtu\.be/[\w-]+'
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    @staticmethod
    def validate_subtitle_format(subtitles: List[Dict[str, Any]]) -> bool:
        """Validate subtitle format."""
        required_fields = {'text', 'start', 'duration'}
        
        try:
            for subtitle in subtitles:
                if not all(field in subtitle for field in required_fields):
                    return False
                if not isinstance(subtitle['text'], str):
                    return False
                if not isinstance(subtitle['start'], (int, float)):
                    return False
                if not isinstance(subtitle['duration'], (int, float)):
                    return False
            return True
        except Exception:
            return False

class ScrapingValidator(BaseValidator):
    """Validator for scraping configuration."""
    
    def __init__(self):
        self.youtube_validator = YouTubeValidator()
        self.scraping_rules = SCRAPING_RULES
    
    def validate(self, config: Dict[str, Any]) -> bool:
        required_fields = {
            'scraping': dict,
            'youtube_api': dict,
            'error_patterns': list
        }
        
        self._validate_required_fields(config, required_fields)
        self._validate_required_fields(config['scraping'], self.scraping_rules)
        
        return True 