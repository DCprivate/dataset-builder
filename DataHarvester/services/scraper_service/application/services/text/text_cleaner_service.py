# Software/DataHarvester/services/scraper_service/application/services/text/text_cleaner_service.py

from infrastructure.logging.logger import get_logger
import re
from typing import List, Dict, Set, Any, Union
import nltk
from nltk.corpus import stopwords
from infrastructure.monitoring.health_checker import HealthChecker
from application.services.text.nlp_service import NLPEngine
from validation.validators.config_validator import validate_settings
from presidio_analyzer import AnalyzerEngine
from pathlib import Path
from infrastructure.config.config_manager import ConfigManager
from domain.exceptions.domain_exceptions import ConfigurationError
import spacy
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult

logger = get_logger()

class TranscriptCleaner:
    def __init__(self):
        """Initialize the TranscriptCleaner with configuration."""
        try:
            # Initialize NLTK components
            nltk.download('popular', quiet=True)  # Download popular datasets including stopwords
            self.stop_words = set(stopwords.words('english'))
            
            # Initialize configuration
            self.config = ConfigManager().get_config('cleaning')
            validate_settings(self.config.get('text_cleaning', {}), {
                'remove': list,
                'preserve': list,
                'normalize': list
            })
            self.settings = self.config.get('text_cleaning', {})
            
            # Initialize NLP components
            self.nlp_engine = NLPEngine()
            self.analyzer = AnalyzerEngine()
            
            # Initialize health checker
            self.health_checker = HealthChecker()
            
            # Setup data paths
            self.data_path = Path('data/processed')
            self.data_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize spaCy
            self.nlp = spacy.load('en_core_web_sm')
            
            # Initialize Anonymizer
            self.anonymizer = AnonymizerEngine()
            
            logger.info("TranscriptCleaner initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TranscriptCleaner: {str(e)}")
            raise ConfigurationError(f"TranscriptCleaner initialization failed: {str(e)}", "CLN001")

    def clean_text(self, text: str) -> str:
        """Clean the input text according to configuration settings."""
        try:
            if not text:
                return ""

            # Health check before processing
            self.health_checker.check_nltk_data()

            # Basic cleaning
            text = self._basic_clean(text)
            
            # Remove stopwords if configured
            if self.settings.get('remove_stopwords', True):
                words = text.split()
                words = [w for w in words if w.lower() not in self.stop_words]
                text = ' '.join(words)

            # Process with NLP engine
            if self.settings.get('use_nlp', True):
                text = self._process_with_spacy(text)

            # Anonymize sensitive information if configured
            if self.settings.get('anonymize', True):
                text = self._anonymize_text(text)

            return text.strip()
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            return text

    def clean_transcript(self, transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean a full transcript while preserving structure."""
        try:
            cleaned_transcript = []
            for entry in transcript:
                cleaned_entry = entry.copy()
                if 'text' in entry:
                    cleaned_entry['text'] = self.clean_text(entry['text'])
                cleaned_transcript.append(cleaned_entry)
            return cleaned_transcript
        except Exception as e:
            logger.error(f"Error cleaning transcript: {str(e)}")
            return transcript

    @property
    def artifacts(self) -> List[str]:
        """Lazy load artifacts from settings."""
        return self.settings['artifacts']

    @property
    def word_fixes(self) -> Dict[str, str]:
        """Lazy load word fixes from settings."""
        return self.settings['word_fixes']

    @property
    def interjections(self) -> Set[str]:
        """Lazy load interjections from settings."""
        return set(self.settings['interjections'])

    def _remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'http\S+|www.\S+', '', text)

    def _anonymize_text(self, text: str) -> str:
        """Remove personal information."""
        analyzer_results = [RecognizerResult(start=r.start, end=r.end, score=r.score, entity_type=r.entity_type) 
                          for r in self.analyzer.analyze(text=text, language='en')]
        return self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results).text

    def _basic_clean(self, text: str) -> str:
        """Basic text cleaning while preserving content."""
        try:
            # Apply cleaning based on settings
            if self.settings.get('lowercase', True):
                text = text.lower()

            # Remove specified elements
            for item in self.settings.get('remove', []):
                if item == 'special_characters':
                    text = re.sub(r'[^\w\s]', '', text)
                elif item == 'extra_whitespace':
                    text = ' '.join(text.split())
                elif item == 'urls':
                    text = re.sub(r'http\S+|www.\S+', '', text)
                elif item == 'emojis':
                    text = text.encode('ascii', 'ignore').decode('ascii')

            return text.strip()
        except Exception as e:
            logger.error(f"Error in basic cleaning: {str(e)}")
            return text

    def _process_with_spacy(self, text: str) -> str:
        """
        Process text while preserving natural language structure.
        Maintains contractions, possessives, pronouns, and proper sentence structure.
        """
        try:
            doc = self.nlp(text)
            words = []
            
            for token in doc:
                # Skip only obvious noise
                if (token.text.lower() in self.interjections or
                    (len(token.text) == 1 and not token.text.lower() in {'a', 'i'})):
                    continue
                    
                # Preserve proper nouns, pronouns, and contractions
                if (token.pos_ in {'PROPN', 'PRON'} or 
                    "'" in token.text or 
                    token.dep_ == 'poss'):  # Preserve possessives
                    words.append(token.text)
                    continue
                
                # Handle lemmatization smartly
                if self.settings['perform_lemmatization']:
                    # Don't lemmatize certain parts of speech
                    if token.pos_ in {'AUX', 'VERB'}:
                        # Preserve tense and form
                        words.append(token.text)
                    else:
                        words.append(token.lemma_)
                else:
                    words.append(token.text)
            
            # Join words and fix spacing around punctuation
            text = ' '.join(words)
            text = re.sub(r'\s+([.,!?;:])', r'\1', text)  # Remove space before punctuation
            text = re.sub(r'([.,!?;:])(\w)', r'\1 \2', text)  # Add space after punctuation
            
            # Capitalize first letter of sentences
            text = '. '.join(s.capitalize() for s in text.split('. '))
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error in _process_with_spacy: {str(e)}")
            return text

    def _should_skip_token(self, token) -> bool:
        """Determine if a token should be skipped based on settings."""
        return (
            token.text.lower() in self.interjections or
            (len(token.text) == 1 and 
             not token.text.lower() in {'a', 'i'} and 
             not token.pos_ in {'PRON', 'DET'})
        )

    @staticmethod
    def clean_transcript_text(text: Union[str, List[str]]) -> List[str]:
        """Clean transcript text."""
        try:
            # If input is a string, wrap it in a list
            if isinstance(text, str):
                text = [text]
            # If input is already a list, create a new list (don't modify original)
            else:
                text = list(text)
                
            # Clean each line
            cleaned = []
            for line in text:
                if not isinstance(line, str):
                    continue
                    
                # Basic cleaning
                line = line.strip()
                if line and line != '[Music]':  # Skip empty lines and music markers
                    cleaned.append(line)
                    
            return cleaned
            
        except Exception as e:
            logger.error(f"Error cleaning transcript: {str(e)}")
            # Return original text in a list if cleaning fails
            return [text] if isinstance(text, str) else list(text) 