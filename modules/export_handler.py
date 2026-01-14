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
        company = customer_context.get('company', '')
        industry = customer_context.get('industry', '')
        business_model = customer_context.get('business_model', '')

        if company:
            p = doc.add_paragraph()
            p.add_run(f'Company: ').bold = True
            p.add_run(company)

        if industry:
            p = doc.add_paragraph()
            p.add_run(f'Industry: ').bold = True
            p.add_run(industry)

        if business_model:
            p = doc.add_paragraph()
            p.add_run(f'Business Model: ').bold = True
            p.add_run(business_model)

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
    Export markdown report to PDF format using WeasyPrint.
    Returns bytes that can be downloaded.
    """
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration

        # Convert markdown to HTML
        html_content = markdown.markdown(
            report_markdown,
            extensions=['tables', 'fenced_code', 'nl2br']
        )

        # Add HTML wrapper with styling
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>O2C AI Agent & MCP Readiness Assessment</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 20px;
                    color: #333;
                }}
                h1 {{
                    color: #2E7D32;
                    border-bottom: 3px solid #2E7D32;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #1565C0;
                    border-bottom: 2px solid #1565C0;
                    padding-bottom: 8px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #7B1FA2;
                    margin-top: 20px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f5f5f5;
                    font-weight: bold;
                }}
                code {{
                    background-color: #f5f5f5;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                }}
                pre {{
                    background-color: #f5f5f5;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                .customer-info {{
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-left: 4px solid #2E7D32;
                    margin-bottom: 30px;
                }}
            </style>
        </head>
        <body>
        """

        # Add customer context
        if customer_context:
            company = customer_context.get('company', '')
            industry = customer_context.get('industry', '')
            business_model = customer_context.get('business_model', '')

            full_html += '<div class="customer-info">'
            if company:
                full_html += f'<p><strong>Company:</strong> {company}</p>'
            if industry:
                full_html += f'<p><strong>Industry:</strong> {industry}</p>'
            if business_model:
                full_html += f'<p><strong>Business Model:</strong> {business_model}</p>'
            full_html += '</div>'

        full_html += html_content
        full_html += """
        </body>
        </html>
        """

        # Generate PDF
        font_config = FontConfiguration()
        html_doc = HTML(string=full_html)
        pdf_bytes = html_doc.write_pdf(font_config=font_config)

        return pdf_bytes

    except ImportError:
        # Fallback if WeasyPrint is not available
        # Return a simple text message
        message = "PDF export requires WeasyPrint library. Please install it with: pip install weasyprint"
        return message.encode('utf-8')


def export_to_markdown(report_markdown: str, customer_context: Dict = None) -> str:
    """
    Export report as markdown (with optional header).
    """
    output = "# O2C AI Agent & MCP Readiness Assessment\n\n"

    if customer_context:
        company = customer_context.get('company', '')
        industry = customer_context.get('industry', '')
        business_model = customer_context.get('business_model', '')

        if company:
            output += f"**Company:** {company}\n\n"
        if industry:
            output += f"**Industry:** {industry}\n\n"
        if business_model:
            output += f"**Business Model:** {business_model}\n\n"

        output += "---\n\n"

    output += report_markdown

    return output
