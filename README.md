# Lecture Quiz Tool (Offline Version)

An interactive Python tool that reads Markdown lecture files and generates quiz questions based on the content. **Fully offline** - no API keys or internet connection required!

## Features

- 📚 Load and parse Markdown lecture files
- 🎯 Generate topic-specific quiz questions using local NLP
- 💬 **Direct Q&A** - Ask questions directly (e.g., "what is narrow ai")
- 🔍 TF-IDF-based semantic search to find relevant content
- ✅ Interactive quiz sessions with fuzzy answer evaluation
- 📊 Performance summary with accuracy percentage
- 🎲 Auto-quiz mode for random questions
- 💾 Optional result export to JSON
- 🚀 **100% Offline** - No external APIs or cloud services

## Requirements

- Python 3.10 or higher
- No internet connection required after initial setup
- No API keys needed

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data (first run only):**
   The tool will automatically download required NLTK data on first run, but you can also do it manually:
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('averaged_perceptron_tagger')
   ```

## Usage

### Basic Usage

```bash
python main.py lecture.md
```

### With Result Saving

```bash
python main.py lecture.md --save
```

### Example Commands

Once the tool is running, you can use these commands:

- **Ask direct questions (Q&A mode):**
  ```
  > what is narrow ai
  > what is machine learning
  > what are intelligent agents
  ```

- **Generate topic-specific questions:**
  ```
  > Give me 5 questions on Scrum cycles
  > Ask me 3 questions about software testing
  > Give me 10 questions on Agile methodology
  > quiz me on machine learning
  ```

- **Auto-quiz mode (random questions):**
  ```
  > autoquiz
  ```

- **Get explanation for a question:**
  ```
  > explain question 2
  ```

- **Quit:**
  ```
  > quit
  ```

## Example Interaction

```
$ python main.py ai_lecture.md

Loading file: ai_lecture.md
✅ File loaded successfully! (5502 characters)
Initializing question generator (this may take a moment)...
✅ Ready!

============================================================
Lecture Quiz Tool (Offline Version)
============================================================

Type a command, e.g.:
  > Give me 5 questions on Agile methodology
  > Ask me 3 questions about software testing
  > what is narrow ai
  > autoquiz
  > explain question 2
  > quit

------------------------------------------------------------

> what is narrow ai

💡 Answer: designed to perform specific tasks. Examples include voice assistants, recommendation systems, and image recognition software.

> Give me 5 questions on machine learning

============================================================
Generating 5 questions on: machine learning
============================================================

Q1: What is Machine Learning?
------------------------------------------------------------
Your answer: a subset of AI
✅ Correct!

Q2: What does Machine Learning enable?
------------------------------------------------------------
Your answer: systems to learn from experience
✅ Correct!

...

============================================================
SUMMARY
============================================================
Total questions: 5
Correct answers: 4
Accuracy: 80.0%
============================================================
```

## Project Structure

```
project_root/
├── main.py               # Entry point for CLI
├── loader.py             # Loads and cleans Markdown files
├── question_generator.py # Generates questions using local NLP and TF-IDF
├── quiz_runner.py        # Handles user interaction and scoring
├── evaluator.py          # Evaluates answers using fuzzy matching
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── example_lecture.md   # Sample lecture file for testing
└── ai_lecture.md        # AI course lecture file
```

## How It Works

1. **Loading**: The `MarkdownLoader` reads and parses the Markdown file, removing formatting and extracting plain text.

2. **Indexing**: The `QuestionGenerator` uses TF-IDF (Term Frequency-Inverse Document Frequency) to create a searchable index of sentences, allowing it to find relevant sections for any topic.

3. **Direct Q&A**: When you ask a direct question (e.g., "what is narrow ai"), the tool:
   - Searches for relevant sentences using TF-IDF
   - Extracts definitions using pattern matching
   - Returns a concise answer from the lecture content

4. **Question Generation**: When you request questions on a topic, the tool:
   - Finds relevant sentences using TF-IDF similarity
   - Applies multiple transformation strategies to convert sentences into questions
   - Ensures the requested number of questions are generated (with fallback strategies)
   - Returns structured questions with answers

5. **Answer Evaluation**: The `AnswerEvaluator` uses:
   - Fuzzy string matching (SequenceMatcher)
   - Keyword overlap analysis
   - Key phrase detection
   - Normalized text comparison

6. **Scoring**: Results are tracked and displayed with a summary at the end.

## Technical Details

### Question Generation Strategies

The tool uses 9 different strategies to generate questions:

1. **Definition Questions**: "What is X?" from "X is Y" patterns
2. **Role Questions**: "Who does X?" from passive/active patterns
3. **Quantity Questions**: "How long/many?" for numeric information
4. **Fill-in-the-Blank**: Removes key terms to create blanks
5. **Comprehension Questions**: "What does X do?" from declarative sentences
6. **Component Questions**: "What are the components/types of X?"
7. **Purpose Questions**: "What is the purpose of X?"
8. **Fallback Definition**: Lenient "What is X?" pattern matching
9. **Explanation Questions**: "Explain: X" for key terms

The tool tries multiple strategies and uses fallback mechanisms to ensure the requested number of questions are generated.

### Answer Evaluation

Answers are evaluated using:
- **Fuzzy Matching**: SequenceMatcher for overall similarity (40% weight)
- **Keyword Overlap**: Jaccard similarity of important keywords (60% weight)
- **Key Phrase Detection**: Checks for important 2-3 word phrases
- **Substring Matching**: Checks if correct answer appears in user answer

Default similarity threshold: 60% (configurable)

## Limitations

- Question quality depends on the structure and clarity of the source material
- Works best with well-structured Markdown files
- May generate simpler questions compared to AI-powered tools
- Answer evaluation is based on text similarity, not semantic understanding
- Direct Q&A works best for definition-style questions

## Troubleshooting

**Error: NLTK data not found**
- The tool will try to download it automatically
- If that fails, manually download: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"`

**Error: File not found**
- Check that the path to your Markdown file is correct
- Use absolute paths if needed

**Questions seem generic or not relevant**
- The tool works best with well-structured Markdown files
- Make sure your file has clear sections and content related to the topics you're asking about
- Try being more specific with your topic queries

**Not enough questions generated**
- The tool now uses multiple fallback strategies to ensure all requested questions are generated
- If you still get fewer questions, try a different topic or use `autoquiz` for general questions
- Make sure your lecture file has enough content on the requested topic

**Q&A not finding answers**
- Try rephrasing your question (e.g., "what is X" instead of "explain X")
- Make sure the term exists in the lecture file
- The tool works best for definition-style questions

## License

This project is provided as-is for educational and personal use.
#   q u i z m d  
 