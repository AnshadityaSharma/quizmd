"""
Module for running interactive quiz sessions.
"""

from typing import List, Dict, Optional
from question_generator import QuestionGenerator
from evaluator import AnswerEvaluator


class QuizRunner:
    """Handles the interactive quiz flow."""
    
    def __init__(self, question_generator: QuestionGenerator):
        """
        Initialize the quiz runner.
        
        Args:
            question_generator: Instance of QuestionGenerator
        """
        self.question_generator = question_generator
        self.evaluator = AnswerEvaluator()
        self.results = []
    
    def run_quiz(
        self, 
        topic: Optional[str] = None, 
        num_questions: int = 5
    ) -> Dict:
        """
        Run an interactive quiz session.
        
        Args:
            topic: Optional topic to focus on
            num_questions: Number of questions to ask
            
        Returns:
            Dictionary with quiz results
        """
        print(f"\n{'='*60}")
        if topic:
            print(f"Generating {num_questions} questions on: {topic}")
        else:
            print(f"Generating {num_questions} general questions")
        print(f"{'='*60}\n")
        
        # Generate questions
        try:
            questions = self.question_generator.generate_questions(topic, num_questions)
        except Exception as e:
            print(f"Error generating questions: {e}")
            import traceback
            traceback.print_exc()
            return {
                "total": 0,
                "correct": 0,
                "accuracy": 0.0,
                "results": []
            }
        
        if not questions:
            print("No questions could be generated from the content.")
            return {
                "total": 0,
                "correct": 0,
                "accuracy": 0.0,
                "results": []
            }
        
        # Ask questions one by one
        self.results = []
        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}: {q['question']}")
            print("-" * 60)
            
            # Get user answer
            user_answer = input("Your answer: ").strip()
            
            if not user_answer:
                print("⚠️  No answer provided. Marking as incorrect.")
                is_correct = False
                feedback = f"Incorrect. The correct answer is: {q['answer']}"
            else:
                # Evaluate answer
                is_correct, feedback = self.evaluator.evaluate_answer(
                    user_answer=user_answer,
                    correct_answer=q['answer'],
                    question=q['question'],
                    context=q.get('context', '')
                )
            
            # Display result
            if is_correct:
                print(f"✅ {feedback}")
            else:
                print(f"❌ {feedback}")
            
            # Store result
            self.results.append({
                "question": q['question'],
                "user_answer": user_answer,
                "correct_answer": q['answer'],
                "is_correct": is_correct,
                "context": q.get('context', '')
            })
            
            # Small pause for readability
            if i < len(questions):
                print()
        
        # Calculate summary
        total = len(self.results)
        correct = sum(1 for r in self.results if r['is_correct'])
        accuracy = (correct / total * 100) if total > 0 else 0.0
        
        # Display summary
        self._display_summary(total, correct, accuracy)
        
        return {
            "total": total,
            "correct": correct,
            "accuracy": accuracy,
            "results": self.results
        }
    
    def _display_summary(self, total: int, correct: int, accuracy: float):
        """Display quiz summary."""
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Total questions: {total}")
        print(f"Correct answers: {correct}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"{'='*60}\n")
    
    def get_results(self) -> List[Dict]:
        """Get the results from the last quiz session."""
        return self.results
    
    def explain_question(self, question_number: int) -> str:
        """
        Provide detailed explanation for a specific question.
        
        Args:
            question_number: 1-based index of the question
            
        Returns:
            Explanation string
        """
        if not self.results or question_number < 1 or question_number > len(self.results):
            return "Question not found. Please run a quiz first."
        
        result = self.results[question_number - 1]
        explanation = f"\nQuestion: {result['question']}\n"
        explanation += f"Correct Answer: {result['correct_answer']}\n"
        if result.get('context'):
            explanation += f"Source: {result['context'][:200]}...\n"
        explanation += f"Your Answer: {result['user_answer']}\n"
        explanation += f"Result: {'✅ Correct' if result['is_correct'] else '❌ Incorrect'}\n"
        
        return explanation

