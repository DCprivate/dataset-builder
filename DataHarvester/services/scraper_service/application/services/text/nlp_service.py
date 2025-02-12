# Software/DataHarvester/services/scraper_service/application/services/text/nlp_service.py

from infrastructure.logging.logger import get_logger
import nltk
import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine
from infrastructure.monitoring.health_checker import HealthChecker

logger = get_logger()

class NLPEngine:
    def __init__(self):
        self.nlp = None
        self.analyzer = None
        self.anonymizer = None
        self.nltk_data_path = '/usr/local/share/nltk_data'
        
    def initialize(self) -> bool:
        """Initialize all NLP components."""
        try:
            # Initialize NLTK
            if not self._init_nltk():
                return False
                
            # Initialize spaCy
            if not self._init_spacy():
                return False
                
            # Initialize Presidio
            if not self._init_presidio():
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP engine: {str(e)}")
            return False
    
    def _init_nltk(self) -> bool:
        """Initialize NLTK components."""
        try:
            nltk.data.path.append(self.nltk_data_path)
            health_ok, missing = HealthChecker().check_nltk_data()
            if not health_ok:
                logger.error(f"Missing NLTK data: {', '.join(missing)}")
                return False
            return True
        except Exception as e:
            logger.error(f"NLTK initialization failed: {str(e)}")
            return False
    
    def _init_spacy(self) -> bool:
        """Initialize spaCy model."""
        try:
            self.nlp = spacy.load('en_core_web_sm')
            return True
        except Exception as e:
            logger.error(f"spaCy initialization failed: {str(e)}")
            return False
    
    def _init_presidio(self) -> bool:
        """Initialize Presidio analyzers."""
        try:
            # Create NLP engine configuration for Presidio
            from presidio_analyzer.nlp_engine import NlpEngineProvider
            configuration = {
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]
            }
            provider = NlpEngineProvider(nlp_configuration=configuration)
            
            # Initialize registry with our configured engine
            registry = RecognizerRegistry()
            registry.load_predefined_recognizers(languages=['en'])
            
            self.analyzer = AnalyzerEngine(
                nlp_engine=provider.create_engine(),
                registry=registry,
                supported_languages=['en'],
                default_score_threshold=0.4
            )
            
            self.anonymizer = AnonymizerEngine()
            return True
        except Exception as e:
            logger.error(f"Presidio initialization failed: {str(e)}")
            return False
    
    def get_nlp(self):
        """Get spaCy NLP model."""
        return self.nlp
    
    def get_analyzer(self):
        """Get Presidio analyzer."""
        return self.analyzer
    
    def get_anonymizer(self):
        """Get Presidio anonymizer."""
        return self.anonymizer 