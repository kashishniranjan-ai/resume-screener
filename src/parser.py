"""
parser.py - Extract and clean text from PDF resumes and job descriptions
"""

import re
import io
from pathlib import Path


def extract_text_from_pdf(file_path: str = None, file_bytes: bytes = None) -> str:
    """
    Extract raw text from a PDF file.
    Accepts either a file path or raw bytes (for Streamlit uploads).
    """
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")

    text = ""
    try:
        if file_bytes:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif file_path:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            raise ValueError("Provide either file_path or file_bytes")
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {e}")

    return clean_text(text)


def extract_text_from_txt(content: str) -> str:
    """Clean and return plain text content."""
    return clean_text(content)


def clean_text(text: str) -> str:
    """Remove noise from extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove weird characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def extract_contact_info(text: str) -> dict:
    """Extract basic contact fields from resume text."""
    info = {}

    # Email
    email_match = re.search(r'[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        info['email'] = email_match.group()

    # Phone
    phone_match = re.search(r'(\+?\d[\d\s\-().]{7,}\d)', text)
    if phone_match:
        info['phone'] = phone_match.group().strip()

    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
    if linkedin_match:
        info['linkedin'] = linkedin_match.group()

    # GitHub
    github_match = re.search(r'github\.com/[\w\-]+', text, re.IGNORECASE)
    if github_match:
        info['github'] = github_match.group()

    return info


def split_resume_sections(text: str) -> dict:
    """
    Attempt to split resume into named sections.
    Returns dict of section_name -> content.
    """
    section_headers = [
        'experience', 'work experience', 'employment', 'education',
        'skills', 'technical skills', 'projects', 'certifications',
        'summary', 'objective', 'achievements', 'publications'
    ]

    pattern = r'(?i)^(' + '|'.join(section_headers) + r')[:\s]*$'
    lines = text.split('\n')
    sections = {}
    current_section = 'header'
    current_content = []

    for line in lines:
        if re.match(pattern, line.strip()):
            sections[current_section] = '\n'.join(current_content).strip()
            current_section = line.strip().lower()
            current_content = []
        else:
            current_content.append(line)

    sections[current_section] = '\n'.join(current_content).strip()
    return sections
