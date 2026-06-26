from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

text = Path('relatorio_final.md').read_text(encoding='utf-8')
lines = [line.rstrip() for line in text.splitlines() if line.strip()]

story = []
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitlePT', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, leading=24, spaceAfter=12))
styles.add(ParagraphStyle(name='HeadingPT', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=16, spaceAfter=8, spaceBefore=8))
styles.add(ParagraphStyle(name='BodyPT', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name='BulletPT', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=14, leftIndent=12, bulletIndent=0, spaceAfter=4))

for line in lines:
    if line.startswith('# '):
        story.append(Paragraph(line[2:], styles['TitlePT']))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:], styles['HeadingPT']))
    elif line.startswith('- '):
        story.append(Paragraph(line[2:], styles['BulletPT']))
    else:
        story.append(Paragraph(line, styles['BodyPT']))
    story.append(Spacer(1, 4))

pdf_path = Path('relatorio_final.pdf')
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
doc.build(story)
print(f'PDF gerado em: {pdf_path.resolve()}')
