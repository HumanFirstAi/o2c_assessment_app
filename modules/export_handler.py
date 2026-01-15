from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO
import markdown
from typing import Dict
import re


def export_to_docx(report_markdown: str, customer_context: Dict = None) -> bytes:
    """
    Export markdown report to DOCX format.
    Returns bytes that can be downloaded.
    """
    doc = Document()

    # Add title
    title = doc.add_heading('O2C AI Agent & MCP Readiness Assessment', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add customer context if provided
    if customer_context:
        user = customer_context.get('user', '')
        email = customer_context.get('email', '')

        if user:
            p = doc.add_paragraph()
            p.add_run(f'Prepared for: ').bold = True
            p.add_run(user)

        if email:
            p = doc.add_paragraph()
            p.add_run(f'Email: ').bold = True
            p.add_run(email)

        doc.add_paragraph()  # Blank line

    # Parse markdown and add to document
    lines = report_markdown.split('\n')
    in_code_block = False
    in_list = False

    for line in lines:
        # Handle code blocks
        if line.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            p = doc.add_paragraph(line)
            p.style = 'List Bullet'
            continue

        # Handle headers
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('#### '):
            doc.add_heading(line[5:], level=4)

        # Handle bullet lists
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Remove markdown bold/italic
            text = text.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
            p = doc.add_paragraph(text, style='List Bullet')

        # Handle numbered lists
        elif re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line).strip()
            text = text.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
            p = doc.add_paragraph(text, style='List Number')

        # Handle tables (basic)
        elif '|' in line and not line.strip().startswith('|--'):
            # Skip for now - table parsing is complex
            continue

        # Handle regular paragraphs
        elif line.strip():
            # Remove markdown formatting
            text = line.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
            if text.strip():
                doc.add_paragraph(text)

        # Blank lines
        else:
            if not in_list:
                doc.add_paragraph()

    # Save to BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()


def export_to_pdf(report_markdown: str, customer_context: Dict = None) -> bytes:
    """
    Export markdown report to PDF format using fpdf2 (pure Python, no system deps).
    Returns bytes that can be downloaded.
    """
    try:
        from fpdf import FPDF

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Set font
        pdf.set_font("Helvetica", size=10)

        # Title
        pdf.set_font("Helvetica", "B", size=16)
        pdf.cell(0, 10, "O2C AI Agent & MCP Readiness Assessment", ln=True, align="C")

        # Customer context
        if customer_context:
            user = customer_context.get('user', '')
            email = customer_context.get('email', '')

            pdf.set_font("Helvetica", size=10)
            if user:
                pdf.cell(0, 6, f"Prepared for: {user}", ln=True, align="C")
            if email:
                pdf.cell(0, 6, f"Email: {email}", ln=True, align="C")

        pdf.ln(10)

        # Process markdown to text
        lines = report_markdown.split('\n')

        for line in lines:
            line = line.strip()

            if not line:
                pdf.ln(5)
                continue

            # Headers
            if line.startswith('### '):
                pdf.set_font("Helvetica", "B", size=12)
                pdf.multi_cell(0, 6, line.replace('### ', ''))
                pdf.set_font("Helvetica", size=10)
            elif line.startswith('## '):
                pdf.set_font("Helvetica", "B", size=14)
                pdf.multi_cell(0, 8, line.replace('## ', ''))
                pdf.set_font("Helvetica", size=10)
            elif line.startswith('# '):
                pdf.set_font("Helvetica", "B", size=16)
                pdf.multi_cell(0, 10, line.replace('# ', ''))
                pdf.set_font("Helvetica", size=10)

            # Bold text
            elif line.startswith('**') and line.endswith('**'):
                pdf.set_font("Helvetica", "B", size=10)
                pdf.multi_cell(0, 6, line.replace('**', ''))
                pdf.set_font("Helvetica", size=10)

            # Bullets
            elif line.startswith('• ') or line.startswith('- ') or line.startswith('* '):
                pdf.set_x(15)  # Indent
                clean_line = line[2:] if line.startswith(('• ', '- ', '* ')) else line
                # Remove markdown formatting
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_line)  # Bold
                clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)  # Italic
                pdf.multi_cell(0, 5, clean_line)

            # Regular text
            else:
                # Remove markdown formatting
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # Bold
                clean_line = re.sub(r'\*(.*?)\*', r'\1', clean_line)  # Italic
                pdf.multi_cell(0, 5, clean_line)

        return pdf.output()

    except Exception as e:
        # Fallback if fpdf2 has issues
        message = f"PDF export error: {str(e)}. Please try Word export instead."
        return message.encode('utf-8')


def export_to_markdown(report_markdown: str, customer_context: Dict = None) -> str:
    """
    Export report as markdown (with optional header).
    """
    output = "# O2C AI Agent & MCP Readiness Assessment\n\n"

    if customer_context:
        user = customer_context.get('user', '')
        email = customer_context.get('email', '')

        if user:
            output += f"**Prepared for:** {user}\n\n"
        if email:
            output += f"**Email:** {email}\n\n"

        output += "---\n\n"

    output += report_markdown

    return output
