# Software/DataHarvester/services/data_ingestion/validation/rules/validation_rules.py

from typing import Dict, Any

# Common validation rules and constants
TEXT_CLEANING_RULES = {
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

DATABASE_CONNECTION_RULES = {
    'uri': str,
    'database': str,
    'max_pool_size': int,
    'min_pool_size': int,
    'max_idle_time_ms': int,
    'connection_timeout_ms': int,
    'server_selection_timeout_ms': int
}

DATABASE_RETRY_RULES = {
    'max_attempts': int,
    'initial_delay': (int, float),
    'max_delay': (int, float),
    'exponential_base': (int, float)
}

SCRAPING_RULES = {
    'delay_between_requests': (int, float),
    'max_retries': int,
    'retry_delay': (int, float),
    'preferred_languages': list,
    'fallback_to_auto_translate': bool,
    'include_auto_generated': bool,
    'batch_size': int,
    'max_concurrent_requests': int,
    'timeout': int
}

def get_validation_rules(rule_type: str) -> Dict[str, Any]:
    """Get validation rules by type."""
    rules = {
        'text_cleaning': TEXT_CLEANING_RULES,
        'database_connection': DATABASE_CONNECTION_RULES,
        'database_retry': DATABASE_RETRY_RULES,
        'scraping': SCRAPING_RULES
    }
    return rules.get(rule_type, {})
