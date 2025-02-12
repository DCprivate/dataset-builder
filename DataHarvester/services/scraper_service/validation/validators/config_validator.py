# Software/DataHarvester/services/scraper_service/validation/validators/config_validator.py

from typing import Dict, Any
from .base_validator import BaseValidator
from domain.exceptions.domain_exceptions import ValidationError, ConfigurationError
from validation.rules.validation_rules import TEXT_CLEANING_RULES, get_validation_rules

REQUIRED_SETTINGS = {
    'remove_timestamps': bool,
    'remove_speaker_labels': bool,
    'remove_special_characters': bool,
    'convert_to_lowercase': bool,
    'remove_urls': bool,
    'remove_email_addresses': bool,
    'remove_phone_numbers': bool,
    'remove_html_tags': bool,
    'remove_stop_words': bool,
    'remove_numbers': bool,
    'remove_single_chars': bool,
    'min_word_length': int,
    'preserve_quotes': bool,
    'preserve_sentence_structure': bool,
    'preserve_proper_nouns': bool,
    'remove_sound_effects': bool,
    'remove_music_annotations': bool,
    'remove_audience_reactions': bool,
    'fix_contractions': bool,
    'fix_spelling': bool,
    'standardize_whitespace': bool,
    'perform_lemmatization': bool,
    'perform_stemming': bool,
    'remove_personal_info': bool,
    'artifacts': list,
    'word_fixes': dict,
    'interjections': list
}

class SettingsValidator(BaseValidator):
    def __init__(self):
        self.required_settings = TEXT_CLEANING_RULES

    def validate(self, settings: Dict[str, Any]) -> bool:
        """Validate settings against required fields and types."""
        try:
            if not isinstance(settings, dict):
                raise ValidationError("Settings must be a dictionary", "VAL004")
            
            return self._validate_required_fields(settings, self.required_settings)
        except ValidationError:
            raise
        except Exception as e:
            raise ValidationError(f"Settings validation failed: {str(e)}", "VAL005")

def validate_settings(settings: Dict[str, Any], required_fields: Dict[str, type]) -> None:
    """
    Validate configuration settings against required fields and their types.
    
    Args:
        settings: Dictionary containing configuration settings
        required_fields: Dictionary mapping field names to their expected types
    
    Raises:
        ConfigurationError: If validation fails
    """
    if not isinstance(settings, dict):
        raise ConfigurationError("Settings must be a dictionary", "CFG001")

    for field, expected_type in required_fields.items():
        if field not in settings:
            raise ConfigurationError(f"Missing required field: {field}", "CFG002")
        
        if not isinstance(settings[field], expected_type):
            raise ConfigurationError(
                f"Invalid type for {field}. Expected {expected_type.__name__}, got {type(settings[field]).__name__}",
                "CFG003"
            )

def validate_cleaning_config(config: Dict[str, Any]) -> None:
    """Validate cleaning configuration."""
    required_fields = {
        "remove": list,
        "preserve": list,
        "lowercase": bool,
        "normalize": list
    }
    validate_settings(config.get("text_cleaning", {}), required_fields)

def validate_harvesting_config(config: Dict[str, Any]) -> None:
    """Validate harvesting configuration."""
    required_fields = {
        "delay_between_requests": (int, float),
        "max_retries": int,
        "retry_delay": (int, float),
        "preferred_languages": list,
        "fallback_to_auto_translate": bool,
        "include_auto_generated": bool,
        "batch_size": int,
        "max_concurrent_requests": int,
        "timeout": int
    }
    
    scraping_config = config.get("scraping", {})
    for field, expected_type in required_fields.items():
        if field not in scraping_config:
            raise ConfigurationError(f"Missing required field in scraping config: {field}", "CFG004")
        
        if isinstance(expected_type, tuple):
            if not isinstance(scraping_config[field], expected_type):
                raise ConfigurationError(
                    f"Invalid type for {field}. Expected one of {[t.__name__ for t in expected_type]}, got {type(scraping_config[field]).__name__}",
                    "CFG005"
                )
        elif not isinstance(scraping_config[field], expected_type):
            raise ConfigurationError(
                f"Invalid type for {field}. Expected {expected_type.__name__}, got {type(scraping_config[field]).__name__}",
                "CFG006"
            )

def validate_database_config(config: Dict[str, Any]) -> None:
    """Validate database configuration."""
    required_fields = {
        "uri": str,
        "database": str,
        "collections": dict,
        "options": dict
    }
    validate_settings(config.get("mongodb", {}), required_fields)

def validate_sources_config(config: Dict[str, Any]) -> None:
    """Validate sources configuration."""
    required_fields = {
        "videos": list,
        "playlists": list,
        "channels": list
    }
    validate_settings(config.get("sources", {}), required_fields) 