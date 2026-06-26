import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

text = Path('relatorio_final.md').read_text(encoding='utf-8')
lines = [line.rstrip() for line in text.splitlines() if line.strip()]

story = []
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitlePT', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=20, leading=24, spaceAfter=12))
styles.add(ParagraphStyle(name='HeadingPT', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=16, spaceAfter=8, spaceBefore=8))
styles.add(ParagraphStyle(name='BodyPT', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=14, spaceAfter=6))
styles.add(ParagraphStyle(name='BulletPT', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.5, leading=14, leftIndent=12, bulletIndent=0, spaceAfter=4))
styles.add(ParagraphStyle(name='CellPT', parent=styles['BodyText'], fontName='Helvetica', fontSize=5.8, leading=7.2, spaceAfter=0))
styles.add(ParagraphStyle(name='CodePT', parent=styles['BodyText'], fontName='Courier-Bold', fontSize=8.2, leading=10, leftIndent=12, rightIndent=12, spaceAfter=4, textColor=colors.HexColor('#333333')))


def build_table(table_rows):
    data = []
    for row in table_rows:
        data.append([Paragraph(cell, styles['CellPT']) for cell in row])

    table = Table(
        data,
        repeatRows=1,
        hAlign='LEFT',
        colWidths=[0.55*inch, 1.0*inch, 0.95*inch, 1.05*inch, 1.45*inch, 0.55*inch],
        splitByRow=1,
    )
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2F4F4F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 5.8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    return table


rows = []
in_code_block = False
code_lines = []

for line in lines:
    if line.startswith('|'):
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if not cells or all(not cell or set(cell.replace('-', '')) == set() for cell in cells):
            continue
        rows.append(cells)
        continue

    if rows:
        if len(rows) > 1:
            story.append(build_table(rows))
            story.append(Spacer(1, 10))
        rows = []

    if line.startswith('```'):
        if in_code_block:
            if code_lines:
                story.append(Paragraph('<br/>'.join(code_lines), styles['CodePT']))
                story.append(Spacer(1, 4))
            code_lines = []
            in_code_block = False
        else:
            in_code_block = True
        continue

    if in_code_block:
        code_lines.append(line)
        continue

    heading_match = re.match(r'^(#{1,6})\s*(.*)$', line)
    if heading_match:
        heading_text = heading_match.group(2).strip()
        if len(heading_match.group(1)) == 1:
            story.append(Paragraph(heading_text, styles['TitlePT']))
        else:
            story.append(Paragraph(heading_text, styles['HeadingPT']))
    elif line.startswith('- '):
        story.append(Paragraph(line[2:], styles['BulletPT']))
    else:
        story.append(Paragraph(line, styles['BodyPT']))
    story.append(Spacer(1, 4))

if in_code_block and code_lines:
    story.append(Paragraph('<br/>'.join(code_lines), styles['CodePT']))
    story.append(Spacer(1, 4))

if rows:
    if len(rows) > 1:
        story.append(build_table(rows))
        story.append(Spacer(1, 10))

pdf_path = Path('relatorio_final.pdf')
doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
doc.build(story)
print(f'PDF gerado em: {pdf_path.resolve()}')
