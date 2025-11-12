"""
Module for generating quiz questions from Markdown content using local NLP.
Uses TF-IDF for topic relevance and simple transformation rules for question generation.
"""

import re
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# Download required NLTK data
def _download_nltk_data():
    """Download required NLTK data if not already present."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        try:
            nltk.download('punkt', quiet=True)
        except Exception:
            print("Warning: Could not download NLTK punkt tokenizer. Some features may not work.")
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            nltk.download('stopwords', quiet=True)
        except Exception:
            print("Warning: Could not download NLTK stopwords. Some features may not work.")
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        try:
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception:
            print("Warning: Could not download NLTK POS tagger. Some features may not work.")

# Download on import
_download_nltk_data()


class QuestionGenerator:
    """Generates quiz questions based on topics in the Markdown content."""
    
    def __init__(self, markdown_content: str):
        """
        Initialize the question generator.
        
        Args:
            markdown_content: The full cleaned content of the Markdown file
        """
        self.markdown_content = markdown_content
        self.sentences = self._extract_sentences()
        self.vectorizer = None
        self.sentence_vectors = None
        self._build_tfidf_index()
    
    def _extract_sentences(self) -> List[str]:
        """
        Extract sentences from the content.
        
        Returns:
            List of sentences
        """
        try:
            # Use NLTK sentence tokenizer
            sentences = sent_tokenize(self.markdown_content)
        except Exception:
            # Fallback: simple regex-based sentence splitting
            sentences = re.split(r'[.!?]+\s+', self.markdown_content)
        
        # Filter out very short sentences (likely artifacts)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def _build_tfidf_index(self):
        """Build TF-IDF index for all sentences."""
        if not self.sentences:
            self.sentences = self._extract_sentences()
        
        if not self.sentences:
            return
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        # Fit and transform sentences
        self.sentence_vectors = self.vectorizer.fit_transform(self.sentences)
    
    def _find_relevant_sentences(self, topic: str, n_sentences: int = 10) -> List[str]:
        """
        Find relevant sentences for a given topic using TF-IDF similarity.
        
        Args:
            topic: The topic to search for
            n_sentences: Number of relevant sentences to return
            
        Returns:
            List of relevant sentences
        """
        if not self.vectorizer or self.sentence_vectors is None:
            # Fallback: keyword matching
            topic_lower = topic.lower()
            topic_words = set(topic_lower.split())
            relevant = []
            for sent in self.sentences:
                sent_lower = sent.lower()
                # Count matching words
                matches = sum(1 for word in topic_words if word in sent_lower)
                if matches > 0:
                    relevant.append((sent, matches))
            relevant.sort(key=lambda x: x[1], reverse=True)
            return [s[0] for s in relevant[:n_sentences]]
        
        # Use TF-IDF similarity
        try:
            topic_vector = self.vectorizer.transform([topic])
            similarities = cosine_similarity(topic_vector, self.sentence_vectors)[0]
            
            # Get top N sentences
            top_indices = similarities.argsort()[-n_sentences:][::-1]
            relevant_sentences = [self.sentences[i] for i in top_indices if similarities[i] > 0.1]
            
            return relevant_sentences[:n_sentences]
        except Exception as e:
            # Fallback to keyword matching
            print(f"Warning: TF-IDF search failed: {e}. Using keyword matching.")
            return self._find_relevant_sentences_keyword(topic, n_sentences)
    
    def _find_relevant_sentences_keyword(self, topic: str, n_sentences: int = 10) -> List[str]:
        """Fallback keyword-based sentence search."""
        topic_lower = topic.lower()
        topic_words = set(topic_lower.split())
        relevant = []
        for sent in self.sentences:
            sent_lower = sent.lower()
            matches = sum(1 for word in topic_words if word in sent_lower)
            if matches > 0:
                relevant.append((sent, matches))
        relevant.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in relevant[:n_sentences]]
    
    def _is_valid_sentence_for_question(self, sentence: str) -> bool:
        """Check if sentence is suitable for question generation."""
        # Must be long enough
        if len(sentence.strip()) < 20:
            return False
        
        # Must have proper capitalization
        if not sentence[0].isupper():
            return False
        
        # Avoid sentences that are just lists or fragments (but be lenient)
        if sentence.count(',') > 8:  # Too many commas (likely a list)
            return False
        
        # Try to check for verb, but don't fail if we can't
        try:
            words = word_tokenize(sentence)
            if len(words) < 5:  # Too short
                return False
            tagged = pos_tag(words)
            has_verb = any(tag.startswith('VB') for _, tag in tagged)
            # Don't require verb if sentence is long enough and has structure
            if not has_verb and len(words) < 10:
                return False
        except:
            # If tokenization fails, just check length
            if len(sentence.split()) < 5:
                return False
        
        return True
    
    def answer_question(self, question: str) -> Optional[str]:
        """
        Answer a direct question by finding relevant content.
        
        Args:
            question: User's question (e.g., "what is narrow ai")
            
        Returns:
            Answer string or None if not found
        """
        # Normalize question
        question_lower = question.lower().strip()
        
        # Remove question words
        question_clean = re.sub(r'^(what|who|where|when|why|how|is|are|does|do|can|will)\s+', '', question_lower)
        question_clean = re.sub(r'\s+(what|who|where|when|why|how|is|are|does|do|can|will)$', '', question_clean)
        question_clean = question_clean.strip()
        
        if not question_clean:
            return None
        
        # Find relevant sentences
        relevant_sentences = self._find_relevant_sentences(question_clean, n_sentences=5)
        
        if not relevant_sentences:
            return None
        
        # Look for definition patterns: "X is Y" or "X, also known as Y, is Z"
        for sentence in relevant_sentences:
            # Pattern 1: "X is Y" or "X, also known as Y, is Z"
            # Try to match the key term flexibly
            question_words = question_clean.split()
            key_term = question_clean  # Full phrase
            last_word = question_words[-1] if question_words else ""
            
            # Build flexible pattern - match if sentence contains the key term
            # Pattern: "X is Y" where X contains the key term
            # Try full phrase first
            if len(question_words) > 1:
                # Multi-word: "narrow ai" -> look for "Narrow AI" or "narrow AI"
                # Create pattern that matches "Narrow AI" or "narrow ai" or "Narrow ai"
                capitalized_phrase = " ".join([w.capitalize() for w in question_words])
                pattern = rf'({re.escape(key_term)}|{re.escape(capitalized_phrase)}|{capitalized_phrase})\s+(?:,\s*also known as\s+[^,]+\s*,)?\s+is\s+([^.]{{10,150}})'
            else:
                # Single word
                pattern = rf'({re.escape(key_term)}|{re.escape(key_term.capitalize())})\s+(?:,\s*also known as\s+[^,]+\s*,)?\s+is\s+([^.]{{10,150}})'
            
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                answer = match.group(2).strip()
                if len(answer) > 150:
                    answer = answer[:150].rsplit(' ', 1)[0] + '...'
                return answer
            
            # Pattern 1b: "X, also known as Y, is Z" - extract the definition after "is"
            pattern_alt = rf'({re.escape(key_term)}|{" ".join([w.capitalize() for w in question_words]) if len(question_words) > 1 else key_term.capitalize()})\s*,\s*also known as\s+[^,]+\s*,\s+is\s+([^.]{{10,150}})'
            match = re.search(pattern_alt, sentence, re.IGNORECASE)
            if match:
                answer = match.group(2).strip()
                if len(answer) > 150:
                    answer = answer[:150].rsplit(' ', 1)[0] + '...'
                return answer
            
            # Pattern 2: "X refers to Y" or "X means Y"
            pattern2 = rf'({re.escape(key_term)}|{" ".join([w.capitalize() for w in question_words]) if len(question_words) > 1 else key_term.capitalize()})\s+(?:refers to|means|denotes)\s+([^.]{{10,150}})'
            match = re.search(pattern2, sentence, re.IGNORECASE)
            if match:
                answer = match.group(2).strip()
                if len(answer) > 150:
                    answer = answer[:150].rsplit(' ', 1)[0] + '...'
                return answer
            
            # Pattern 3: "X, also known as Y" - return the alternative name
            pattern3 = rf'({re.escape(key_term)}|{" ".join([w.capitalize() for w in question_words]) if len(question_words) > 1 else key_term.capitalize()})\s*,\s*also known as\s+([^,]+)'
            match = re.search(pattern3, sentence, re.IGNORECASE)
            if match:
                answer = f"Also known as {match.group(2).strip()}"
                return answer
        
        # Fallback: return the most relevant sentence
        if relevant_sentences:
            answer = relevant_sentences[0]
            if len(answer) > 200:
                answer = answer[:200].rsplit(' ', 1)[0] + '...'
            return answer
        
        return None
    
    def _generate_question_from_sentence(self, sentence: str) -> Optional[Dict[str, str]]:
        """
        Generate a question from a sentence using transformation rules.
        
        Args:
            sentence: The source sentence
            
        Returns:
            Dictionary with 'question' and 'answer' keys, or None if generation fails
        """
        sentence = sentence.strip()
        if len(sentence) < 20:
            return None
        
        # Remove trailing punctuation for processing
        original_sentence = sentence
        sentence = sentence.rstrip('.!?')
        
        # Try different question generation strategies
        question = None
        answer = None
        
        # Strategy 1: "What is X?" from "X is Y" patterns - IMPROVED
        match = re.search(r'^([A-Z][a-zA-Z\s]{3,40}?)\s+is\s+([^.]{10,100})', sentence, re.IGNORECASE)
        if match:
            subject = match.group(1).strip()
            definition = match.group(2).strip()
            
            # Validate subject doesn't contain verbs or action words
            if not re.search(r'\b(uses|does|performs|facilitates|manages|involves)\b', subject, re.IGNORECASE):
                # Clean up subject (remove trailing words that don't belong)
                subject = re.sub(r'\s+(is|are|was|were|the|a|an)$', '', subject, flags=re.IGNORECASE)
                # Limit answer length
                if len(definition) > 100:
                    definition = definition[:100].rsplit(' ', 1)[0] + '...'
                question = f"What is {subject}?"
                answer = definition
        
        # Strategy 2: "Who/What does X?" from passive/active patterns
        if not question:
            # Look for "X is done by Y" or "Y does X"
            match = re.search(r'([A-Z][a-zA-Z\s]{5,40}) (?:is|are) (?:done by|performed by|led by|facilitated by|responsible for) ([A-Z][a-zA-Z\s]{3,50})', sentence, re.IGNORECASE)
            if match:
                action = match.group(1).strip()
                actor = match.group(2).strip()
                # Clean up actor name
                actor = re.split(r'[,\s]+', actor)[0]  # Take first part
                if len(actor) > 30:
                    actor = actor[:30]
                question = f"Who {action.lower()}?"
                answer = actor
        
        # Strategy 3: "How long/How many" for numbers
        if not question:
            match = re.search(r'([A-Z][^.]{5,}) (?:is|are|lasts|takes) (?:typically|usually|generally|about|approximately)?\s*(\d+)\s+(\w+)', sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                number = match.group(2)
                unit = match.group(3)
                question = f"How long is {subject.lower()}?" if unit in ['week', 'weeks', 'day', 'days', 'hour', 'hours'] else f"How many {unit} is {subject.lower()}?"
                answer = f"{number} {unit}"
        
        # Strategy 4: Fill-in-the-blank by removing key noun phrases
        if not question:
            # Try to identify important noun phrases and create blanks
            try:
                words = word_tokenize(sentence)
                tagged = pos_tag(words)
            except Exception:
                # Fallback: simple word splitting
                words = sentence.split()
                tagged = [(w, 'NN') for w in words]  # Default to noun
            
            # Find noun phrases (sequences of nouns/adjectives)
            important_terms = []
            current_phrase = []
            for word, tag in tagged:
                if tag.startswith('NN') or tag.startswith('JJ'):
                    current_phrase.append(word)
                else:
                    if len(current_phrase) >= 2 and len(current_phrase) <= 4:
                        important_terms.append(' '.join(current_phrase))
                    current_phrase = []
            if len(current_phrase) >= 2 and len(current_phrase) <= 4:
                important_terms.append(' '.join(current_phrase))
            
            if important_terms:
                # Use a medium-length important term as the answer (not too long)
                important_terms.sort(key=len)
                # Pick a term that's 3-5 words, or the longest if all are shorter
                answer_term = None
                for term in important_terms:
                    if 3 <= len(term.split()) <= 5:
                        answer_term = term
                        break
                if not answer_term and important_terms:
                    answer_term = important_terms[-1]  # Use longest
                
                if answer_term and 5 < len(answer_term) < 50:  # Reasonable length
                    # Create question by replacing the term
                    question = sentence.replace(answer_term, "_____", 1)
                    # Limit question length
                    if len(question) > 150:
                        # Try to shorten
                        words = question.split()
                        if len(words) > 20:
                            question = ' '.join(words[:20]) + '...'
                    answer = answer_term
        
        # Strategy 5: "What" question from declarative sentences - IMPROVED
        if not question:
            # Avoid matching "X uses Y" as "What does X do?" - be more specific
            # Only match if there's a clear action verb
            match = re.search(r'^([A-Z][a-zA-Z\s]{3,30}?)\s+(?:performs|facilitates|manages|handles|executes)\s+([^.]{10,80})', sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                action = match.group(2).strip()
                # Skip if subject is too generic (like "Finance", "Healthcare")
                generic_subjects = ['finance', 'healthcare', 'transportation', 'e-commerce', 'industry', 'field', 'domain']
                if subject.lower() not in generic_subjects:
                    # Clean up subject
                    subject = re.sub(r'\s+(performs|facilitates|manages|handles|executes)$', '', subject, flags=re.IGNORECASE)
                    # Limit answer length
                    if len(action) > 80:
                        action = action[:80].rsplit(' ', 1)[0] + '...'
                    question = f"What does {subject} do?"
                    answer = action
        
        # Strategy 6: "What are the types/components of X?"
        if not question:
            # Look for lists or types: "X includes Y, Z, W" - but be more careful
            # Match at the start of sentence to avoid partial matches
            match = re.search(r'^([A-Z][a-zA-Z\s]{3,30}?)\s+(?:includes|consists of|has|contains)\s+([^.]{10,100})', sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                items = match.group(2).strip()
                # Clean up subject - remove trailing words
                subject = re.sub(r'\s+(includes|consists|has|contains|are|is|of)$', '', subject, flags=re.IGNORECASE)
                # Validate subject is reasonable (not too long, not containing verbs)
                if len(subject) > 40 or re.search(r'\b(uses|does|performs|enables)\b', subject, re.IGNORECASE):
                    match = None
                else:
                    # Limit answer
                    if len(items) > 80:
                        items = items[:80].rsplit(' ', 1)[0] + '...'
                    question = f"What are the components or types of {subject}?"
                    answer = items
        
        # Strategy 7: "What is the purpose/role of X?"
        if not question:
            # Look for purpose/role statements
            match = re.search(r'^([A-Z][a-zA-Z\s]{5,40}?)\s+(?:is|are)\s+(?:used for|designed to|aims to|purpose is|role is)\s+([^.]{10,80})', sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                purpose = match.group(2).strip()
                # Clean up
                subject = re.sub(r'\s+(is|are|used|designed|aims|purpose|role)$', '', subject, flags=re.IGNORECASE)
                if len(purpose) > 80:
                    purpose = purpose[:80].rsplit(' ', 1)[0] + '...'
                question = f"What is the purpose of {subject}?"
                answer = purpose
        
        # Strategy 8: Fallback - simple "What is X?" from any "X is Y" pattern
        if not question:
            # Very lenient pattern - just find "X is Y" anywhere
            match = re.search(r'([A-Z][a-zA-Z\s]{3,35}?)\s+is\s+([^.]{15,100})', sentence)
            if match:
                subject = match.group(1).strip()
                definition = match.group(2).strip()
                # Skip if subject contains common verbs (already tried in Strategy 1)
                if not re.search(r'\b(uses|does|performs|facilitates|manages|involves|enables|allows)\b', subject, re.IGNORECASE):
                    # Clean up
                    subject = re.sub(r'\s+(is|are|was|were|the|a|an)$', '', subject, flags=re.IGNORECASE)
                    if len(subject) < 50 and len(definition) > 10:
                        if len(definition) > 100:
                            definition = definition[:100].rsplit(' ', 1)[0] + '...'
                        question = f"What is {subject}?"
                        answer = definition
        
        # Strategy 9: Last resort - "Explain X" where X is a key term
        if not question:
            if len(sentence) > 30:
                try:
                    words = word_tokenize(sentence)
                    tagged = pos_tag(words)
                    # Find important nouns (proper nouns or capitalized nouns)
                    important_words = []
                    for word, tag in tagged:
                        if (tag.startswith('NNP') or (tag.startswith('NN') and word[0].isupper() and len(word) > 4)):
                            important_words.append(word)
                    
                    if important_words:
                        key_term = important_words[0]
                        # Use a portion of the sentence as answer
                        answer_text = sentence[:120] if len(sentence) > 120 else sentence
                        question = f"Explain: {key_term}"
                        answer = answer_text
                except:
                    pass
        
        # If we still don't have a question, skip this sentence
        if not question:
            return None
        
        # Clean up answer
        if answer:
            answer = answer.strip().rstrip('.!?')
            # Remove extra whitespace
            answer = ' '.join(answer.split())
            # Limit answer length strictly
            if len(answer) > 100:
                answer = answer[:100].rsplit(' ', 1)[0] + '...'
        
        # Clean up question
        if question:
            question = question.strip()
            # Remove extra whitespace
            question = ' '.join(question.split())
            # Limit question length
            if len(question) > 200:
                question = question[:200].rsplit(' ', 1)[0] + '...'
        
        # Final validation
        if question and answer and len(question) > 10 and len(answer) > 5:
            return {
                "question": question,
                "answer": answer,
                "context": original_sentence[:200]  # Limit context too
            }
        
        return None
    
    def generate_questions(
        self, 
        topic: Optional[str] = None, 
        num_questions: int = 5
    ) -> List[Dict[str, str]]:
        """
        Generate quiz questions based on the content.
        
        Args:
            topic: Optional topic to focus on. If None, uses random sentences.
            num_questions: Number of questions to generate
            
        Returns:
            List of question dictionaries with 'question', 'answer', and 'context' keys
        """
        questions = []
        seen_questions = set()  # Avoid duplicates
        max_attempts = num_questions * 10  # Try many more sentences than needed
        
        # First, try to get questions from topic-relevant sentences
        if topic:
            # Find relevant sentences for the topic
            relevant_sentences = self._find_relevant_sentences(topic, n_sentences=max_attempts)
        else:
            # Use random sentences from the entire content
            import random
            relevant_sentences = random.sample(
                self.sentences, 
                min(max_attempts, len(self.sentences))
            ) if len(self.sentences) > num_questions else self.sentences
        
        # Filter sentences for validity (but be less strict)
        valid_sentences = [s for s in relevant_sentences if self._is_valid_sentence_for_question(s)]
        
        # If we don't have enough valid sentences, relax the validation
        if len(valid_sentences) < num_questions * 2:
            # Use a more lenient filter
            valid_sentences = [s for s in relevant_sentences if len(s.strip()) > 20 and s[0].isupper()]
        
        # Generate questions from sentences
        consecutive_failures = 0
        for sentence in valid_sentences:
            if len(questions) >= num_questions:
                break
            
            q_data = self._generate_question_from_sentence(sentence)
            if q_data:
                # Check for duplicates
                q_key = q_data['question'].lower()
                if q_key not in seen_questions:
                    seen_questions.add(q_key)
                    questions.append(q_data)
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
            else:
                consecutive_failures += 1
            
            # Only break if we've tried many sentences without success
            if consecutive_failures > 50:
                break
        
        # If we still don't have enough questions, try more sentences from entire content
        if len(questions) < num_questions:
            import random
            # Get more sentences, excluding ones we've already tried
            tried_sentences = set(valid_sentences)
            remaining_sentences = [s for s in self.sentences if s not in tried_sentences]
            
            if remaining_sentences:
                # Try more sentences
                additional_sentences = random.sample(
                    remaining_sentences,
                    min(num_questions * 5, len(remaining_sentences))
                )
                
                # Filter for validity (lenient)
                additional_valid = [s for s in additional_sentences if len(s.strip()) > 20 and s[0].isupper()]
                
                for sentence in additional_valid:
                    if len(questions) >= num_questions:
                        break
                    
                    q_data = self._generate_question_from_sentence(sentence)
                    if q_data:
                        q_key = q_data['question'].lower()
                        if q_key not in seen_questions:
                            seen_questions.add(q_key)
                            questions.append(q_data)
        
        # If we still don't have enough, try even more lenient question generation
        if len(questions) < num_questions:
            # Try all remaining sentences with minimal filtering
            all_remaining = [s for s in self.sentences if len(s.strip()) > 15]
            import random
            random.shuffle(all_remaining)
            
            for sentence in all_remaining:
                if len(questions) >= num_questions:
                    break
                
                # Skip if we've already generated a question from this sentence
                if sentence in tried_sentences:
                    continue
                
                q_data = self._generate_question_from_sentence(sentence)
                if q_data:
                    q_key = q_data['question'].lower()
                    if q_key not in seen_questions:
                        seen_questions.add(q_key)
                        questions.append(q_data)
        
        return questions[:num_questions]

