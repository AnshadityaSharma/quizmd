"""
Main entry point for the Lecture Quiz Tool (Offline Version).
"""

import argparse
import sys
import json
import random
from loader import MarkdownLoader
from question_generator import QuestionGenerator
from quiz_runner import QuizRunner


def parse_command(command: str) -> tuple:
    """
    Parse user command to extract topic and number of questions.
    
    Args:
        command: User input command string
        
    Returns:
        Tuple of (topic, num_questions, command_type, question_text)
    """
    command_original = command.strip()
    command = command_original.lower()
    
    # Check for special commands
    if command == "autoquiz":
        return None, None, "autoquiz", None
    
    if command.startswith("explain question"):
        try:
            parts = command.split()
            q_num = int(parts[-1])
            return None, q_num, "explain", None
        except:
            return None, None, "invalid", None
    
    # Check for direct Q&A questions (starts with what/who/where/when/why/how/is/are/does/do/can/will)
    import re
    if re.match(r'^(what|who|where|when|why|how|is|are|does|do|can|will)', command):
        return None, None, "qa", command_original
    
    # Parse regular question requests
    # Look for patterns like "give me 5 questions on X" or "ask me 3 questions about X"
    
    # Extract number
    num_match = re.search(r'(\d+)', command)
    num_questions = int(num_match.group(1)) if num_match else 5
    
    # Extract topic
    topic = None
    if "on " in command:
        topic = command.split("on ", 1)[1].strip()
    elif "about " in command:
        topic = command.split("about ", 1)[1].strip()
    elif "regarding " in command:
        topic = command.split("regarding ", 1)[1].strip()
    
    # Clean up topic
    if topic:
        # Remove common question words at the end
        topic = re.sub(r'\s+(questions?|quiz|test)$', '', topic, flags=re.IGNORECASE)
        topic = topic.strip()
    
    return topic, num_questions, "quiz", None


def run_autoquiz(quiz_runner: QuizRunner, num_questions: int = 7):
    """Run an auto quiz with random questions from across the file."""
    print("\n🎲 Running Auto Quiz...")
    return quiz_runner.run_quiz(topic=None, num_questions=num_questions)


def save_results(results: dict, filename: str = "quiz_results.json"):
    """Save quiz results to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ Results saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Interactive quiz tool for lecture Markdown files (Offline Version)"
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the Markdown file"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save quiz results to a JSON file"
    )
    
    args = parser.parse_args()
    
    # Load the Markdown file
    print(f"Loading file: {args.file}")
    try:
        loader = MarkdownLoader(args.file)
        raw_content = loader.load()
        content = loader.clean_markdown()
        print(f"✅ File loaded successfully! ({len(content)} characters)")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)
    
    # Initialize components
    try:
        print("Initializing question generator (this may take a moment)...")
        question_generator = QuestionGenerator(content)
        quiz_runner = QuizRunner(question_generator)
        print("✅ Ready!\n")
    except Exception as e:
        print(f"❌ Error initializing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Interactive loop
    print("=" * 60)
    print("Lecture Quiz Tool (Offline Version)")
    print("=" * 60)
    print("\nType a command, e.g.:")
    print("  > Give me 5 questions on Agile methodology")
    print("  > Ask me 3 questions about software testing")
    print("  > what is narrow ai")
    print("  > autoquiz")
    print("  > explain question 2")
    print("  > quit")
    print("\n" + "-" * 60 + "\n")
    
    while True:
        try:
            command = input("> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            # Parse command
            topic, num_questions, cmd_type, question_text = parse_command(command)
            
            if cmd_type == "autoquiz":
                results = run_autoquiz(quiz_runner)
                if args.save:
                    save_results(results)
            
            elif cmd_type == "explain":
                if num_questions:
                    explanation = quiz_runner.explain_question(num_questions)
                    print(explanation)
                else:
                    print("Invalid question number.")
            
            elif cmd_type == "qa":
                # Direct Q&A
                answer = question_generator.answer_question(question_text)
                if answer:
                    print(f"\n💡 Answer: {answer}\n")
                else:
                    print(f"\n❌ I couldn't find an answer to that question in the lecture.\n")
            
            elif cmd_type == "quiz":
                results = quiz_runner.run_quiz(
                    topic=topic if topic else None,
                    num_questions=num_questions
                )
                if args.save:
                    save_results(results)
            
            else:
                print("❌ Invalid command. Try:")
                print("  > Give me 5 questions on [topic]")
                print("  > what is [topic]")
                print("  > autoquiz")
                print("  > explain question [number]")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

