# Software/DataHarvester/services/scraper_service/infrastructure/config/config_manager.py

from pathlib import Path
import yaml
from typing import Dict, Any
from infrastructure.logging.logger import get_logger
from validation.validators.database_validator import DatabaseValidator
from validation.validators.scraping_validator import ScrapingValidator
from domain.exceptions.domain_exceptions import ConfigurationError

logger = get_logger()

class ConfigManager:
    _instance = None
    _validators = {
        'database': DatabaseValidator(),
        'harvesting': ScrapingValidator()
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.configs = {}
            self._load_configs()
            self.validate_configs()
        
    def _load_configs(self):
        """Load all configuration files."""
        config_dir = Path("/app/config")
        config_files = {
            'database': 'database.yaml',
            'cleaning': 'cleaning.yaml',
            'harvesting': 'harvesting.yaml',
            'sources': 'sources.yaml'
        }
        
        for config_type, filename in config_files.items():
            file_path = config_dir / filename
            try:
                with open(file_path, 'r') as f:
                    self.configs[config_type] = yaml.safe_load(f)
                logger.info(f"Loaded configuration: {config_type}")
            except Exception as e:
                logger.error(f"Failed to load {config_type} configuration: {str(e)}")
                raise ConfigurationError(
                    f"Failed to load configuration file {filename}",
                    "CFG001"
                )
            
    def validate_configs(self):
        """Validate loaded configurations."""
        for config_type, validator in self._validators.items():
            if config_type not in self.configs:
                raise ConfigurationError(
                    f"Missing configuration for {config_type}",
                    "CFG003"
                )
            try:
                validator.validate(self.configs[config_type])
                logger.info(f"Validated configuration: {config_type}")
            except Exception as e:
                raise ConfigurationError(
                    f"Configuration validation failed for {config_type}: {str(e)}",
                    "CFG004"
                )
            
    def get_config(self, config_type: str) -> Dict[str, Any]:
        """Get configuration by type."""
        if config_type == 'scraping':
            config_type = 'harvesting'
        if config_type not in self.configs:
            raise ValueError(f"Configuration type not found: {config_type}")
        return self.configs[config_type] 