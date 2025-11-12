"""
Module for loading and parsing Markdown files.
Extracts clean, plain-text content for question generation.
"""

import re
from typing import List, Dict


class MarkdownLoader:
    """Handles loading and parsing of Markdown files into plain text."""
    
    def __init__(self, file_path: str):
        """
        Initialize the loader with a file path.
        
        Args:
            file_path: Path to the Markdown file
        """
        self.file_path = file_path
        self.content = ""
        self.sections = []
        self.sentences = []
    
    def load(self) -> str:
        """
        Load the Markdown file content.
        
        Returns:
            The raw content of the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            IOError: If there's an error reading the file
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return self.content
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except IOError as e:
            raise IOError(f"Error reading file {self.file_path}: {str(e)}")
    
    def clean_markdown(self) -> str:
        """
        Remove Markdown formatting and extract plain text.
        
        Returns:
            Cleaned plain text content
        """
        if not self.content:
            self.load()
        
        text = self.content
        
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove images
        text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
        
        # Remove headers but keep text (convert # to nothing)
        text = re.sub(r'^#{1,6}\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^\*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Remove horizontal rules
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\*\*\*+$', '', text, flags=re.MULTILINE)
        
        # Remove list markers
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text.strip()
    
    def get_sections(self) -> List[Dict[str, str]]:
        """
        Parse the Markdown content into sections based on headers.
        
        Returns:
            List of dictionaries with 'title' and 'content' keys
        """
        if not self.content:
            self.load()
        
        sections = []
        lines = self.content.split('\n')
        current_section = {"title": "Introduction", "content": ""}
        
        for line in lines:
            # Check for headers (markdown headers start with #)
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)
                
                # Start new section
                title = header_match.group(2).strip()
                current_section = {"title": title, "content": ""}
            else:
                # Add line to current section
                current_section["content"] += line + "\n"
        
        # Add the last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        self.sections = sections
        return sections
    
    def get_full_content(self) -> str:
        """
        Get the full cleaned content of the loaded file.
        
        Returns:
            The complete cleaned file content
        """
        return self.clean_markdown()

