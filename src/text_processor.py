"""
Text Processor Module
Handles text processing, validation, and enhancement.
"""

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TextProcessor:
    """Handles text processing and validation."""
    
    def __init__(self):
        """Initialize TextProcessor."""
        self.max_length = 5000
        self.min_length = 10
        logger.info("TextProcessor initialized")
    
    def validate_text(self, text: str) -> tuple[bool, str]:
        """
        Validate text input.
        
        Args:
            text: Text to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not text:
            return False, "Text cannot be empty"
        
        text = text.strip()
        
        if len(text) < self.min_length:
            return False, f"Text must be at least {self.min_length} characters"
        
        if len(text) > self.max_length:
            return False, f"Text must not exceed {self.max_length} characters"
        
        return True, "Text is valid"
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def enhance_for_video(self, text: str, style: str = "cinematic") -> str:
        """
        Enhance text for better video generation.
        
        Args:
            text: Original text
            style: Video style
            
        Returns:
            Enhanced text
        """
        # Add descriptive words based on style
        style_enhancers = {
            "cinematic": [
                "professional",
                "high quality",
                "4K",
                "cinematic lighting",
            ],
            "documentary": [
                "educational",
                "informative",
                "detailed",
                "natural",
            ],
            "animation": [
                "colorful",
                "vibrant",
                "animated",
                "cartoon-style",
            ],
            "scifi": [
                "futuristic",
                "advanced technology",
                "sci-fi",
                "high-tech",
            ],
            "natural": [
                "realistic",
                "authentic",
                "natural lighting",
                "organic",
            ],
        }
        
        enhancers = style_enhancers.get(style, [])
        
        # Add enhancers to the text
        if enhancers:
            enhanced_text = f"{', '.join(enhancers)}: {text}"
            return enhanced_text
        
        return text
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def estimate_duration(self, text: str, wpm: int = 150) -> int:
        """
        Estimate video duration based on text length.
        
        Args:
            text: Text content
            wpm: Words per minute (default 150 for normal speech)
            
        Returns:
            Estimated duration in seconds
        """
        word_count = len(text.split())
        duration_minutes = word_count / wpm
        duration_seconds = int(duration_minutes * 60)
        
        # Minimum 15 seconds, maximum 60 seconds
        return max(15, min(60, duration_seconds))
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key words from text.
        
        Args:
            text: Text to process
            top_n: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        from collections import Counter
        
        # Convert to lowercase and split
        words = text.lower().split()
        
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "by", "from", "is", "are",
            "was", "were", "be", "been", "being", "have", "has",
            "had", "do", "does", "did", "will", "would", "should",
            "could", "can", "may", "might", "must", "shall",
        }
        
        filtered_words = [
            w for w in words
            if w not in stop_words and len(w) > 2
        ]
        
        # Count word frequency
        word_freq = Counter(filtered_words)
        
        # Get top words
        keywords = [word for word, _ in word_freq.most_common(top_n)]
        
        return keywords
    
    def generate_subtitle_chunks(
        self,
        text: str,
        max_chars_per_line: int = 42,
    ) -> List[str]:
        """
        Generate subtitle chunks from text.
        
        Args:
            text: Full text
            max_chars_per_line: Maximum characters per line
            
        Returns:
            List of subtitle chunks
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > max_chars_per_line:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [word]
                    current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text and provide metrics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with analysis metrics
        """
        sentences = self.split_into_sentences(text)
        words = text.split()
        keywords = self.extract_keywords(text)
        duration = self.estimate_duration(text)
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "average_word_length": sum(len(w) for w in words) / len(words) if words else 0,
            "keywords": keywords,
            "estimated_duration": duration,
            "sentences": sentences,
        }
