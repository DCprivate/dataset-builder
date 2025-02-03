# Software/DataHarvester/src/infrastructure/error_handling/utils/text_utils.py

import re
from typing import List

def format_error_message(message: str, context: str | None = None) -> str:
    """Format error message with context."""
    if context:
        return f"[{context}] {message}"
    return message

def chunk_error_log(text: str, max_length: int = 1000) -> List[str]:
    """Split error log into chunks of maximum length while preserving lines."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length <= max_length:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks 