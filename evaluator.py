"""
Module for evaluating user answers against correct answers.
Uses fuzzy string matching and keyword comparison.
"""

from typing import Tuple
from difflib import SequenceMatcher
import re


class AnswerEvaluator:
    """Evaluates user answers against correct answers using local matching."""
    
    def __init__(self, similarity_threshold: float = 0.6):
        """
        Initialize the evaluator.
        
        Args:
            similarity_threshold: Minimum similarity score (0-1) to consider an answer correct
        """
        self.similarity_threshold = similarity_threshold
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def _extract_keywords(self, text: str) -> set:
        """
        Extract important keywords from text.
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            Set of keywords
        """
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        words = self._normalize_text(text).split()
        keywords = {w for w in words if len(w) > 2 and w not in stop_words}
        return keywords
    
    def _fuzzy_match(self, text1: str, text2: str) -> float:
        """
        Calculate fuzzy similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        norm1 = self._normalize_text(text1)
        norm2 = self._normalize_text(text2)
        
        if not norm1 or not norm2:
            return 0.0
        
        # Use SequenceMatcher for overall similarity
        similarity = SequenceMatcher(None, norm1, norm2).ratio()
        
        # Also check keyword overlap
        keywords1 = self._extract_keywords(text1)
        keywords2 = self._extract_keywords(text2)
        
        if keywords1 and keywords2:
            overlap = len(keywords1 & keywords2)
            union = len(keywords1 | keywords2)
            keyword_similarity = overlap / union if union > 0 else 0.0
            
            # Combine both metrics (weighted average)
            combined = (similarity * 0.4) + (keyword_similarity * 0.6)
            return combined
        
        return similarity
    
    def _check_key_phrases(self, user_answer: str, correct_answer: str) -> bool:
        """
        Check if user answer contains key phrases from correct answer.
        
        Args:
            user_answer: User's answer
            correct_answer: Correct answer
            
        Returns:
            True if key phrases match
        """
        user_norm = self._normalize_text(user_answer)
        correct_norm = self._normalize_text(correct_answer)
        
        # Extract important phrases (2-3 word combinations)
        correct_words = correct_norm.split()
        if len(correct_words) < 2:
            return False
        
        # Check for 2-word phrases
        phrases = []
        for i in range(len(correct_words) - 1):
            phrase = f"{correct_words[i]} {correct_words[i+1]}"
            if len(phrase) > 5:  # Only substantial phrases
                phrases.append(phrase)
        
        # Check if any phrase appears in user answer
        for phrase in phrases:
            if phrase in user_norm:
                return True
        
        # Also check for individual important words
        important_words = [w for w in correct_words if len(w) > 4]
        matches = sum(1 for w in important_words if w in user_norm)
        
        # If more than half of important words match, consider it correct
        return matches >= len(important_words) * 0.5 if important_words else False
    
    def evaluate_answer(
        self, 
        user_answer: str, 
        correct_answer: str,
        question: str = "",
        context: str = ""
    ) -> Tuple[bool, str]:
        """
        Evaluate if the user's answer is correct.
        
        Args:
            user_answer: The answer provided by the user
            correct_answer: The correct answer from the question
            question: The original question text (optional)
            context: Optional context (not used in offline version)
            
        Returns:
            Tuple of (is_correct: bool, feedback: str)
        """
        if not user_answer.strip():
            return False, f"Incorrect. The correct answer is: {correct_answer}"
        
        # Normalize answers
        user_norm = self._normalize_text(user_answer)
        correct_norm = self._normalize_text(correct_answer)
        
        # Exact match (after normalization)
        if user_norm == correct_norm:
            return True, "Correct!"
        
        # Check if user answer contains the correct answer (or vice versa)
        if correct_norm in user_norm:
            return True, "Correct!"
        if user_norm in correct_norm and len(user_norm) > len(correct_norm) * 0.7:
            return True, "Correct!"
        
        # Fuzzy matching
        similarity = self._fuzzy_match(user_answer, correct_answer)
        
        if similarity >= self.similarity_threshold:
            return True, "Correct!"
        
        # Check key phrases
        if self._check_key_phrases(user_answer, correct_answer):
            return True, "Correct!"
        
        # Answer is incorrect
        feedback = f"Incorrect. The correct answer is: {correct_answer}"
        if similarity > 0.3:
            feedback += f" (Your answer was close: {similarity:.0%} similar)"
        
        return False, feedback

