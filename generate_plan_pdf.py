#!/usr/bin/env python3
"""Generate MASTER_PLAN.pdf — professional PDF of Sector Intelligence master plan."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# ─── Brand Colors ────────────────────────────────────────────
CS_BLUE = HexColor('#003366')
CS_RED = HexColor('#E30613')
CS_LIGHT_BLUE = HexColor('#e8f0f8')
CS_LIGHT_RED = HexColor('#fde8e8')
CS_LIGHT_GREEN = HexColor('#e8f5e9')
CS_LIGHT_YELLOW = HexColor('#fff8e1')
CS_GRAY = HexColor('#64748b')
CS_LIGHT_GRAY = HexColor('#f1f5f9')
CS_BORDER = HexColor('#e2e8f0')
CS_DARK = HexColor('#1e293b')
CS_GREEN = HexColor('#16a34a')
CS_YELLOW = HexColor('#ca8a04')
CS_ORANGE = HexColor('#ea580c')

OUTPUT_PATH = '/Users/davidnavratil/pracovni/sector-intelligence/MASTER_PLAN.pdf'
W, H = A4  # 595 x 842 points

# ─── Styles ──────────────────────────────────────────────────
def make_styles():
    s = {}
    s['title'] = ParagraphStyle('Title', fontSize=28, leading=34, textColor=CS_BLUE,
                                 fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=4)
    s['subtitle'] = ParagraphStyle('Subtitle', fontSize=14, leading=18, textColor=CS_GRAY,
                                    fontName='Helvetica', alignment=TA_LEFT, spaceAfter=20)
    s['h1'] = ParagraphStyle('H1', fontSize=18, leading=24, textColor=CS_BLUE,
                              fontName='Helvetica-Bold', spaceBefore=20, spaceAfter=10)
    s['h2'] = ParagraphStyle('H2', fontSize=14, leading=18, textColor=CS_BLUE,
                              fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8)
    s['h3'] = ParagraphStyle('H3', fontSize=11, leading=15, textColor=CS_DARK,
                              fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
    s['body'] = ParagraphStyle('Body', fontSize=9.5, leading=14, textColor=CS_DARK,
                                fontName='Helvetica', spaceAfter=6)
    s['body_bold'] = ParagraphStyle('BodyBold', fontSize=9.5, leading=14, textColor=CS_DARK,
                                     fontName='Helvetica-Bold', spaceAfter=6)
    s['small'] = ParagraphStyle('Small', fontSize=8, leading=11, textColor=CS_GRAY,
                                 fontName='Helvetica', spaceAfter=4)
    s['bullet'] = ParagraphStyle('Bullet', fontSize=9.5, leading=14, textColor=CS_DARK,
                                  fontName='Helvetica', leftIndent=16, spaceAfter=3,
                                  bulletIndent=6, bulletFontSize=9)
    s['toc'] = ParagraphStyle('TOC', fontSize=11, leading=18, textColor=CS_DARK,
                               fontName='Helvetica', spaceAfter=4)
    s['toc_num'] = ParagraphStyle('TOCNum', fontSize=11, leading=18, textColor=CS_BLUE,
                                   fontName='Helvetica-Bold', spaceAfter=4)
    s['cell'] = ParagraphStyle('Cell', fontSize=8, leading=11, textColor=CS_DARK,
                                fontName='Helvetica')
    s['cell_bold'] = ParagraphStyle('CellBold', fontSize=8, leading=11, textColor=CS_DARK,
                                     fontName='Helvetica-Bold')
    s['cell_small'] = ParagraphStyle('CellSmall', fontSize=7, leading=10, textColor=CS_GRAY,
                                      fontName='Helvetica')
    s['label_qw'] = ParagraphStyle('LabelQW', fontSize=8, leading=11, textColor=HexColor('#0d6efd'),
                                    fontName='Helvetica-Bold')
    s['label_build'] = ParagraphStyle('LabelBuild', fontSize=8, leading=11, textColor=CS_ORANGE,
                                       fontName='Helvetica-Bold')
    s['label_disc'] = ParagraphStyle('LabelDisc', fontSize=8, leading=11, textColor=HexColor('#7c3aed'),
                                      fontName='Helvetica-Bold')
    return s

S = make_styles()

# ─── Helpers ─────────────────────────────────────────────────
def p(text, style='body'):
    return Paragraph(text, S[style])

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=CS_BORDER, spaceAfter=8, spaceBefore=8)

def badge(label, bg_color, text_color=white):
    """Inline badge as mini table."""
    style = ParagraphStyle('badge', fontSize=7, leading=9, textColor=text_color,
                            fontName='Helvetica-Bold', alignment=TA_CENTER)
    t = Table([[Paragraph(label, style)]], colWidths=[55], rowHeights=[16])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('ROUNDEDCORNERS', [4,4,4,4]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    return t

def make_table(headers, rows, col_widths=None, header_bg=CS_BLUE, zebra=True):
    """Create a styled table."""
    data = [headers] + rows
    if not col_widths:
        avail = W - 80
        col_widths = [avail / len(headers)] * len(headers)

    # Wrap text in Paragraphs
    wrapped = []
    for i, row in enumerate(data):
        new_row = []
        for j, cell in enumerate(row):
            if isinstance(cell, str):
                style = S['cell_bold'] if i == 0 else S['cell']
                if i == 0:
                    style = ParagraphStyle('HeaderCell', fontSize=8, leading=11,
                                           textColor=white, fontName='Helvetica-Bold')
                new_row.append(Paragraph(cell, style))
            else:
                new_row.append(cell)
        wrapped.append(new_row)

    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, CS_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, CS_LIGHT_GRAY] if zebra else [white]),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

def label_tag(text):
    """Return colored label text for Quick win / Build / Discovery."""
    if 'Quick win' in text:
        return '<font color="#0d6efd"><b>Quick win</b></font>'
    elif 'Build' in text:
        return '<font color="#ea580c"><b>Build</b></font>'
    elif 'Discovery' in text:
        return '<font color="#7c3aed"><b>Discovery</b></font>'
    elif 'Hotovo' in text:
        return '<font color="#16a34a"><b>Hotovo</b></font>'
    return text

# ─── Page Templates ──────────────────────────────────────────
def title_page_bg(canvas_obj, doc):
    """Draw title page background."""
    c = canvas_obj
    # Blue header bar
    c.setFillColor(CS_BLUE)
    c.rect(0, H - 200, W, 200, fill=1, stroke=0)
    # Red accent line
    c.setFillColor(CS_RED)
    c.rect(0, H - 205, W, 5, fill=1, stroke=0)
    # Footer
    c.setFillColor(CS_GRAY)
    c.setFont('Helvetica', 8)
    c.drawString(40, 30, 'Sector Intelligence | Ceska sporitelna | Duverny dokument')

def normal_page_bg(canvas_obj, doc):
    """Draw normal page header/footer."""
    c = canvas_obj
    # Top line
    c.setStrokeColor(CS_BLUE)
    c.setLineWidth(2)
    c.line(40, H - 30, W - 40, H - 30)
    # Header text
    c.setFillColor(CS_BLUE)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(40, H - 25, 'Sector Intelligence — Master plan')
    c.setFillColor(CS_RED)
    c.drawRightString(W - 40, H - 25, 'Ceska sporitelna')
    # Footer
    c.setStrokeColor(CS_BORDER)
    c.setLineWidth(0.5)
    c.line(40, 40, W - 40, 40)
    c.setFillColor(CS_GRAY)
    c.setFont('Helvetica', 7)
    c.drawString(40, 28, 'Duverny dokument | Aktualizovano: 23. brezna 2026')
    c.drawRightString(W - 40, 28, f'Strana {doc.page}')

# ─── Build Document ──────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        topMargin=45, bottomMargin=55, leftMargin=40, rightMargin=40
    )
    story = []
    avail_w = W - 80

    # ═══════════════════════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════════════════════
    story.append(Spacer(1, 120))
    story.append(Paragraph('Sector Intelligence', ParagraphStyle(
        'BigTitle', fontSize=36, leading=42, textColor=white,
        fontName='Helvetica-Bold', alignment=TA_LEFT)))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Master plan', ParagraphStyle(
        'BigSub', fontSize=24, leading=30, textColor=HexColor('#99bbdd'),
        fontName='Helvetica', alignment=TA_LEFT)))
    story.append(Spacer(1, 60))
    story.append(Paragraph('Ceska sporitelna · Sektorova analyza', S['subtitle']))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Aktualizovano: 23. brezna 2026', S['body']))
    story.append(Paragraph('Stav: Prototyp webove platformy hotovy, nasazeny na GitHub Pages', S['body']))
    story.append(Spacer(1, 30))

    # Classification legend
    legend_data = [
        ['Klasifikace', 'Vyznam', 'Akce'],
        [Paragraph('<font color="#0d6efd"><b>Quick win</b></font>', S['cell']),
         'Hodiny az dny, jasne zadani, zadne zavislosti', 'Udelat hned'],
        [Paragraph('<font color="#ea580c"><b>Build</b></font>', S['cell']),
         'Tydny, slozitejsi implementace, vime co a jak', 'Naplanovat a realizovat'],
        [Paragraph('<font color="#7c3aed"><b>Discovery</b></font>', S['cell']),
         'Overit proveditelnost, data, procesy, licence', 'Prozkoumat pred rozhodnutim'],
    ]
    legend_t = make_table(legend_data[0], legend_data[1:],
                          col_widths=[avail_w*0.2, avail_w*0.5, avail_w*0.3],
                          header_bg=CS_DARK)
    story.append(legend_t)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════════════════════
    story.append(p('Obsah', 'h1'))
    story.append(hr())
    toc_items = [
        ('1', 'Dekompozice stavajiciho procesu'),
        ('2', 'Architektura datoveho pipeline'),
        ('3', 'Vylepseni analytickeho obsahu'),
        ('4', 'Foresighting framework'),
        ('5', 'Supply chain analyza'),
        ('6', 'Webova platforma'),
        ('7', 'Executive summary a traffic lights'),
        ('8', 'Export reportu'),
        ('9', 'Multi-sector architektura'),
        ('10', 'Uzivatelske role a pristupy'),
        ('11', 'AI-powered funkce'),
        ('12', 'Banking-specificke funkce'),
        ('13', 'Rizika implementace'),
        ('14', 'Roadmap a prioritizace'),
        ('15', 'Metriky uspechu'),
        ('16', 'Discovery backlog'),
        ('17', 'Principy implementace'),
    ]
    for num, title in toc_items:
        story.append(Paragraph(
            f'<font color="#003366"><b>{num}.</b></font>&nbsp;&nbsp;{title}',
            S['toc']))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 1. DEKOMPOZICE
    # ═══════════════════════════════════════════════════════════
    story.append(p('1. Dekompozice stavajiciho procesu', 'h1'))
    story.append(hr())
    story.append(p('Soucasny workflow pripravy sektoroveho reportu (automotive)', 'h2'))

    rows1 = [
        ['1', 'Sber dat z CSU, Eurostatu, ACEA, OICA', '3-4 hod', 'Plne', label_tag('Build')],
        ['2', 'Cisteni a konsolidace dat v Excelu', '2-3 hod', 'Plne', label_tag('Build')],
        ['3', 'Tvorba grafu a tabulek', '2-3 hod', 'Plne', label_tag('Hotovo')],
        ['4', 'Analyza trendu a komentare', '3-4 hod', 'Castecne (AI+revize)', label_tag('Discovery')],
        ['5', 'Monitoring zprav a udalosti', '1-2 hod', 'Plne', label_tag('Build')],
        ['6', 'Identifikace rizik a prilezitosti', '2-3 hod', 'Castecne', label_tag('Discovery')],
        ['7', 'Formatovani a finalizace reportu', '1-2 hod', 'Plne', label_tag('Build')],
        ['8', 'Distribuce', '0.5 hod', 'Plne', label_tag('Quick win')],
    ]
    # Wrap label_tag cells in Paragraphs
    for row in rows1:
        row[4] = Paragraph(row[4], S['cell'])
    t1 = make_table(
        ['Krok', 'Cinnost', 'Cas', 'Automatizace', 'Stitek'],
        rows1,
        col_widths=[avail_w*0.07, avail_w*0.40, avail_w*0.12, avail_w*0.22, avail_w*0.19]
    )
    story.append(t1)
    story.append(Spacer(1, 6))
    story.append(p('<b>Celkem: 15-22 hodin na report</b>', 'body_bold'))

    story.append(Spacer(1, 12))
    story.append(p('Cilovy stav po automatizaci', 'h2'))

    rows1b = [
        ['1-3', 'Automaticky pipeline + web', '0 hod (auto)', '-8-10 hod'],
        ['4', 'AI draft komentaru + revize', '1-1.5 hod', '-2-3 hod'],
        ['5', 'Automaticky monitoring + alerty', '0 hod (auto)', '-1-2 hod'],
        ['6', 'Foresighting framework + AI', '1 hod', '-1-2 hod'],
        ['7', 'Automaticky export PDF/PPTX', '0 hod (auto)', '-1-2 hod'],
        ['8', 'Automaticka distribuce', '0 hod (auto)', '-0.5 hod'],
    ]
    t1b = make_table(
        ['Krok', 'Cinnost', 'Cas (cilovy)', 'Uspora'],
        rows1b,
        col_widths=[avail_w*0.08, avail_w*0.42, avail_w*0.22, avail_w*0.28]
    )
    story.append(t1b)
    story.append(Spacer(1, 6))

    # Savings highlight box
    savings_box = Table(
        [[Paragraph('<b>Cilovy stav: 2-2.5 hodiny na report (~85 % uspora)</b>',
                    ParagraphStyle('Savings', fontSize=11, leading=15, textColor=CS_GREEN,
                                   fontName='Helvetica-Bold', alignment=TA_CENTER))]],
        colWidths=[avail_w])
    savings_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CS_LIGHT_GREEN),
        ('ROUNDEDCORNERS', [6,6,6,6]),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(savings_box)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 2. ARCHITEKTURA PIPELINE
    # ═══════════════════════════════════════════════════════════
    story.append(p('2. Architektura datoveho pipeline', 'h1'))
    story.append(hr())

    story.append(p('2.1 Datove zdroje', 'h2'))
    src_rows = [
        ['CSU API', 'Prumyslova produkce, registrace, zamestnanost', 'Mesicne', Paragraph(label_tag('Build'), S['cell'])],
        ['Eurostat API', 'EU produkce, obchodni bilance, EV registrace', 'Mesicne', Paragraph(label_tag('Build'), S['cell'])],
        ['ACEA', 'Registrace novych vozidel EU, EV podily', 'Mesicne', Paragraph(label_tag('Discovery'), S['cell'])],
        ['ECB/CNB', 'Urokove sazby, menove kurzy', 'Denne', Paragraph(label_tag('Quick win'), S['cell'])],
        ['NewsAPI', 'Monitoring zprav automotive', 'Realtime', Paragraph(label_tag('Quick win'), S['cell'])],
        ['OECD', 'Ekonomicke indikatory, PMI', 'Mesicne', Paragraph(label_tag('Build'), S['cell'])],
        ['UN Comtrade', 'Mezinarodni obchod HS 8703', 'Ctvrtletne', Paragraph(label_tag('Discovery'), S['cell'])],
        ['Bloomberg/Reuters', 'Financni data dodavatelu', 'Denne', Paragraph(label_tag('Discovery'), S['cell'])],
        ['S&P Global', 'Produkcni forecasty', 'Ctvrtletne', Paragraph(label_tag('Discovery'), S['cell'])],
        ['Interni data CS', 'Portfolio, NPL, rating klientu', 'Denne', Paragraph(label_tag('Discovery'), S['cell'])],
    ]
    t2 = make_table(
        ['Zdroj', 'Data', 'Frekvence', 'Stitek'],
        src_rows,
        col_widths=[avail_w*0.18, avail_w*0.42, avail_w*0.18, avail_w*0.22]
    )
    story.append(t2)

    story.append(Spacer(1, 12))
    story.append(p('2.2 Technicka architektura', 'h2'))

    # Pipeline diagram as styled table
    def arch_box(title, desc, bg_color):
        return Table([[
            Paragraph(f'<b>{title}</b><br/><font size="7" color="#64748b">{desc}</font>',
                      ParagraphStyle('ArchBox', fontSize=9, leading=13, textColor=CS_DARK,
                                     fontName='Helvetica-Bold', alignment=TA_CENTER))
        ]], colWidths=[avail_w - 20])

    boxes = [
        ('DATA SOURCES', 'CSU | Eurostat | ACEA | ECB/CNB | NewsAPI | OICA | IEA | Bloomberg', CS_LIGHT_BLUE),
        ('PYTHON DATA PIPELINE', 'fetch_*.py  ->  validate.py  ->  clean_transform.py  ->  generate_data_js.py\n+ ai_commentary.py | detect_anomalies.py | news_classifier.py', CS_LIGHT_YELLOW),
        ('GITHUB ACTIONS (scheduled)', 'Tydne/mesicne: run pipeline -> validate -> commit data.js -> deploy -> notify', CS_LIGHT_GREEN),
        ('WEB PLATFORM (GitHub Pages)  [HOTOVO]', 'index.html + app.js + data.js\nhttps://davidnavratil.github.io/sector-intelligence/', CS_LIGHT_GREEN),
        ('INTERNI PLATFORMA CS (budoucnost) [Discovery]', 'Backend (Python/Node) + Auth + interni data CS', CS_LIGHT_RED),
    ]
    for title, desc, bg in boxes:
        box = Table([[
            Paragraph(f'<b>{title}</b><br/><font size="7" color="#64748b">{desc}</font>',
                      ParagraphStyle('AB', fontSize=9, leading=13, textColor=CS_DARK,
                                     fontName='Helvetica-Bold', alignment=TA_CENTER))
        ]], colWidths=[avail_w])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('ROUNDEDCORNERS', [6,6,6,6]),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(box)
        # Arrow
        story.append(Paragraph('<font color="#003366" size="14">&#x25BC;</font>',
                               ParagraphStyle('Arrow', alignment=TA_CENTER, spaceAfter=2, spaceBefore=2)))
    # Remove last arrow
    story.pop()
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 3-5 Condensed sections
    # ═══════════════════════════════════════════════════════════
    story.append(p('3. Vylepseni analytickeho obsahu', 'h1'))
    story.append(hr())

    for sub_title, items in [
        ('Forward-looking sekce', [
            ('Predikce na 4Q dopredu', 'Build', 'ARIMA, lin. regrese'),
            ('Leading indicators (PMI, objednavky)', 'Build', 'OECD, CSU data'),
            ('Benchmark CR vs. DE, SK, PL, HU', 'Build', 'Eurostat data'),
            ('ML predikcni modely (XGBoost, Prophet)', 'Discovery', 'Dostatek hist. dat?'),
            ('Sentiment analyza trhu', 'Discovery', 'Kvalita ceskych NLP modelu'),
        ]),
        ('Automaticke komentare (Claude API)', [
            ('AI draft ke kazde metrice', 'Discovery', 'Prompt engineering, cost'),
            ('Human-in-the-loop review UI', 'Build', 'Approve/edit/reject workflow'),
            ('Komentare pro relationship managery', 'Discovery', 'Format, relevance'),
            ('Feedback loop (few-shot learning)', 'Build', 'Ukladani do JSON/DB'),
        ]),
        ('Anomalie a alerty', [
            ('Statisticka detekce (z-score, IQR)', 'Build', 'Standardni statistika'),
            ('Traffic light prechody (notifikace)', 'Quick win', 'Logika v pipeline'),
            ('Email / Slack notifikace', 'Quick win', 'Webhook / Sendgrid'),
            ('Eskalacni matice', 'Discovery', 'Interni procesy, stakeholders'),
        ]),
    ]:
        story.append(p(sub_title, 'h3'))
        rows = [[item[0], Paragraph(label_tag(item[1]), S['cell']), item[2]] for item in items]
        t = make_table(['Prvek', 'Stitek', 'Poznamka'], rows,
                       col_widths=[avail_w*0.35, avail_w*0.20, avail_w*0.45])
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 4. FORESIGHTING
    # ═══════════════════════════════════════════════════════════
    story.append(p('4. Foresighting framework', 'h1'))
    story.append(hr())

    story.append(p('4.1 Trend Radar', 'h2'))
    done_box = Table([[Paragraph('<b>Prototyp hotovy</b> — 14 trendu na interaktivnim radaru, vizualizace dopad x horizont',
                                  ParagraphStyle('Done', fontSize=9, leading=13, textColor=CS_GREEN,
                                                 fontName='Helvetica-Bold', alignment=TA_CENTER))]],
                     colWidths=[avail_w])
    done_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CS_LIGHT_GREEN),
        ('ROUNDEDCORNERS', [6,6,6,6]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(done_box)
    story.append(Spacer(1, 8))

    story.append(p('Mechanismus pravidelne aktualizace:', 'h3'))
    update_rows = [
        ['Mesicne', 'Review signalu a monitoring', 'Analytik + AI'],
        ['Ctvrtletne', 'Aktualizace pozic na radaru', 'Analyticky tym'],
        ['Pololetne', 'Pridani/odebrani trendu, validace', 'Tym + externi'],
        ['Rocne', 'Kompletni revize radaru', 'Management + tym'],
    ]
    story.append(make_table(['Frekvence', 'Cinnost', 'Kdo'], update_rows,
                            col_widths=[avail_w*0.2, avail_w*0.5, avail_w*0.3]))
    story.append(Spacer(1, 8))

    story.append(p('Kategorie trendu:', 'h3'))
    for cat in ['Regulatorni (EU emisni limity, CBAM, ESG, Euro 7)',
                'Technologicke (EV, autonomni rizeni, SDV, solid-state baterie)',
                'Trzni (cinska konkurence, konsolidace OEM, subscription modely)',
                'Geopoliticke (nearshoring, trade wars, supply chain diverzifikace)',
                'Socialni (car sharing, urbanizace, demograficke zmeny)',
                'Financni (zelene dluhopisy, ESG investice, stranded assets ICE)']:
        story.append(Paragraph(f'&bull;&nbsp;{cat}', S['bullet']))

    story.append(Spacer(1, 10))
    story.append(p('4.2 Scenarova matice 2x2', 'h2'))
    story.append(p('Osy: Rychlost EV tranzice (pomala - rychla) x Globalni obchodni prostredi (protekcionismus - otevrenost)', 'body'))

    sc_rows = [
        ['Evoluce', 'Pomala tranzice + otevrenost', 'Gradualni adaptace'],
        ['Zeleny boom', 'Rychla tranzice + otevrenost', 'Prilezitost pro early adopters'],
        ['Stagnace', 'Pomala tranzice + protekcionismus', 'Regionalizace'],
        ['Disruption', 'Rychla tranzice + protekcionismus', 'Chaoticka transformace'],
    ]
    story.append(make_table(['Scenar', 'Podminky', 'Dusledek'], sc_rows,
                            col_widths=[avail_w*0.2, avail_w*0.4, avail_w*0.4]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 5. SUPPLY CHAIN
    # ═══════════════════════════════════════════════════════════
    story.append(p('5. Supply chain analyza', 'h1'))
    story.append(hr())

    # Value chain diagram
    tiers = [
        ('Tier 3+\nSuroviny', CS_LIGHT_RED, 'Lithium, Kobalt,\nOcel, Vzacne zeminy'),
        ('Tier 2\nKomponenty', CS_LIGHT_YELLOW, 'Odlitky, Vylisky,\nKabelove svazky'),
        ('Tier 1\nSystemy', CS_LIGHT_BLUE, 'Bateriove packy,\nPodvozkove dily'),
        ('OEM\nVyrobci', CS_LIGHT_GREEN, 'Skoda Auto,\nHyundai, Toyota'),
    ]
    tier_cells = []
    for name, bg, desc in tiers:
        tier_cells.append(Table([[
            Paragraph(f'<b>{name}</b><br/><font size="6" color="#64748b">{desc}</font>',
                      ParagraphStyle('Tier', fontSize=9, leading=12, textColor=CS_DARK,
                                     fontName='Helvetica-Bold', alignment=TA_CENTER))
        ]], colWidths=[avail_w*0.22]))
        tier_cells[-1].setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('ROUNDEDCORNERS', [6,6,6,6]),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))

    arrow_p = Paragraph('<font color="#003366" size="16">&#x25B6;</font>',
                        ParagraphStyle('Arr', alignment=TA_CENTER, fontSize=16))
    chain = Table([[tier_cells[0], arrow_p, tier_cells[1], arrow_p, tier_cells[2], arrow_p, tier_cells[3]]],
                  colWidths=[avail_w*0.22, avail_w*0.04, avail_w*0.22, avail_w*0.04, avail_w*0.22, avail_w*0.04, avail_w*0.22])
    chain.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(chain)
    story.append(Spacer(1, 12))

    story.append(p('Rozsirena supply chain analyza:', 'h3'))
    sc_ext = [
        ['Supplier financial health', 'Discovery', 'Propojeni s bankovnimi daty CS'],
        ['Concentration risk', 'Discovery', 'Data o zavislostech?'],
        ['Nearshoring monitor', 'Build', 'Monitoring zprav + CzechInvest'],
        ['ESG supply chain scoring', 'Discovery', 'Metodika, data, regulace'],
        ['Semiconductor dependency', 'Build', 'Verejna data + odhady'],
        ['Battery supply chain', 'Build', 'IEA data, verejne zdroje'],
        ['Critical raw materials', 'Build', 'EU/USGS data, commodity feeds'],
    ]
    sc_ext_rows = [[r[0], Paragraph(label_tag(r[1]), S['cell']), r[2]] for r in sc_ext]
    story.append(make_table(['Prvek', 'Stitek', 'Poznamka'], sc_ext_rows,
                            col_widths=[avail_w*0.30, avail_w*0.18, avail_w*0.52]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 6-8 Platform, Executive, Export
    # ═══════════════════════════════════════════════════════════
    story.append(p('6. Webova platforma', 'h1'))
    story.append(hr())
    done_box2 = Table([[Paragraph(
        '<b>HOTOVO</b> — https://davidnavratil.github.io/sector-intelligence/<br/>'
        '<font size="7" color="#64748b">HTML + Tailwind CSS + Chart.js | 7 stranek | Svetly theme, CS brand barvy</font>',
        ParagraphStyle('Done2', fontSize=10, leading=14, textColor=CS_GREEN,
                       fontName='Helvetica-Bold', alignment=TA_CENTER))]], colWidths=[avail_w])
    done_box2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CS_LIGHT_GREEN),
        ('ROUNDEDCORNERS', [6,6,6,6]),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(done_box2)
    story.append(Spacer(1, 8))

    web_items = [
        ['Drill-down v grafech', 'Quick win'], ['YoY toggle', 'Quick win'],
        ['Fullscreen mod', 'Quick win'], ['Print-friendly CSS', 'Quick win'],
        ['Dark/light mode toggle', 'Quick win'], ['Responsivni design', 'Build'],
        ['Data download (CSV/Excel)', 'Build'], ['PWA (offline mode)', 'Build'],
        ['Accessibility (WCAG 2.1)', 'Build'], ['Search across all data', 'Build'],
    ]
    web_rows = [[r[0], Paragraph(label_tag(r[1]), S['cell'])] for r in web_items]
    story.append(make_table(['Vylepseni', 'Stitek'], web_rows,
                            col_widths=[avail_w*0.65, avail_w*0.35]))

    story.append(Spacer(1, 12))
    story.append(p('8. Export reportu', 'h1'))
    story.append(hr())
    exp_items = [
        ['PDF export z dashboardu', 'Build', 'jsPDF / WeasyPrint'],
        ['PPTX sablona CS', 'Discovery', 'Existuje brand book?'],
        ['PPTX generator', 'Build', 'python-pptx'],
        ['Excel export dat', 'Quick win', 'SheetJS'],
        ['Automaticka distribuce email', 'Quick win', 'Sendgrid + cron'],
        ['Slack notifikace', 'Quick win', 'Webhook'],
        ['Teams notifikace', 'Discovery', 'Ma CS Teams?'],
        ['SharePoint archivace', 'Discovery', 'Pristup, API'],
    ]
    exp_rows = [[r[0], Paragraph(label_tag(r[1]), S['cell']), r[2]] for r in exp_items]
    story.append(make_table(['Prvek', 'Stitek', 'Poznamka'], exp_rows,
                            col_widths=[avail_w*0.35, avail_w*0.18, avail_w*0.47]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 9. MULTI-SECTOR
    # ═══════════════════════════════════════════════════════════
    story.append(p('9. Multi-sector architektura', 'h1'))
    story.append(hr())

    sector_rows = [
        ['Automotive (NACE 29)', Paragraph(label_tag('Hotovo'), S['cell']), 'Prototyp na webu'],
        ['Energetika (NACE 35)', Paragraph(label_tag('Build'), S['cell']), 'Dostatek verejnych dat'],
        ['IT & Telco (NACE 61-63)', Paragraph(label_tag('Discovery'), S['cell']), 'Specificka data - CTU?'],
        ['Stavebnictvi (NACE 41-43)', Paragraph(label_tag('Build'), S['cell']), 'CSU stavebni produkce'],
        ['Chemie & farma (NACE 20-21)', Paragraph(label_tag('Discovery'), S['cell']), 'Heterogenni sektor'],
        ['Zemedelstvi (NACE 01-03)', Paragraph(label_tag('Discovery'), S['cell']), 'SZIF, EAGRI - API?'],
        ['Logistika (NACE 49-53)', Paragraph(label_tag('Discovery'), S['cell']), 'Fragmentovana data'],
        ['Turismus (NACE 55-56)', Paragraph(label_tag('Discovery'), S['cell']), 'Sezonnost, CSU'],
    ]
    story.append(make_table(['Sektor', 'Stitek', 'Poznamka'], sector_rows,
                            col_widths=[avail_w*0.35, avail_w*0.18, avail_w*0.47]))

    story.append(Spacer(1, 12))
    story.append(p('10. Uzivatelske role', 'h1'))
    story.append(hr())
    role_rows = [
        ['Sektorovy analytik', 'Plny pristup, editace scenaru', 'Build'],
        ['Management', 'Executive dashboard, PDF export', 'Quick win (view-only)'],
        ['Relationship manager', 'Banking, prilezitosti, alerty', 'Discovery'],
        ['Risk manager', 'Supply chain rizika, NPL, stress testy', 'Discovery'],
        ['Ekonomicky vyzkum', 'Makro data, cross-sector', 'Discovery'],
    ]
    role_rows2 = [[r[0], r[1], Paragraph(label_tag(r[2]), S['cell'])] for r in role_rows]
    story.append(make_table(['Role', 'Potreby', 'Stitek'], role_rows2,
                            col_widths=[avail_w*0.25, avail_w*0.45, avail_w*0.30]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 11-12 AI + Banking
    # ═══════════════════════════════════════════════════════════
    story.append(p('11. AI-powered funkce', 'h1'))
    story.append(hr())

    for sub, items in [
        ('Automaticke komentare', [
            ('Claude API integrace', 'Build'), ('Prompt engineering', 'Discovery'),
            ('Human-in-the-loop review UI', 'Build'), ('Few-shot learning', 'Discovery'),
            ('Cost management', 'Discovery'),
        ]),
        ('Detekce anomalii', [
            ('z-score detekce', 'Build'), ('Sezonni adjustace (STL)', 'Build'),
            ('Kontextualni AI vysvetleni', 'Discovery'), ('False positive tuning', 'Discovery'),
        ]),
        ('Monitoring zprav', [
            ('NewsAPI integrace', 'Quick win'), ('Klicova slova per sektor', 'Quick win'),
            ('AI klasifikace (typ + dopad)', 'Discovery'), ('RSS feed monitoring', 'Quick win'),
            ('Deduplikace zprav', 'Build'),
        ]),
        ('Q&A nad daty', [
            ('Chat interface na webu', 'Build'), ('RAG nad data + reporty', 'Discovery'),
            ('Guardrails (sektorove dotazy)', 'Discovery'),
        ]),
    ]:
        story.append(p(sub, 'h3'))
        rows = [[i[0], Paragraph(label_tag(i[1]), S['cell'])] for i in items]
        story.append(make_table(['Prvek', 'Stitek'], rows,
                                col_widths=[avail_w*0.65, avail_w*0.35]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(p('12. Banking-specificke funkce', 'h1'))
    story.append(hr())
    bank_rows = [
        ['Portfolio exposure dashboard', 'Hotovo (demo)', 'Realna data = Discovery'],
        ['NPL monitoring', 'Hotovo (demo)', 'Realna data = Discovery'],
        ['Stress test scenare', 'Discovery', 'Propojeni s risk modely'],
        ['Early warning signals', 'Discovery', 'ML modely, interni data'],
        ['Competitor benchmarking', 'Discovery', 'Verejne vyrocni zpravy, CNB'],
        ['Green finance prilezitosti', 'Discovery', 'Interni produkty CS'],
        ['Regulatorni dopady (DORA, CRR III)', 'Build', 'Monitoring regulace'],
    ]
    bank_rows2 = [[r[0], Paragraph(label_tag(r[1]), S['cell']), r[2]] for r in bank_rows]
    story.append(make_table(['Prvek', 'Stitek', 'Poznamka'], bank_rows2,
                            col_widths=[avail_w*0.35, avail_w*0.18, avail_w*0.47]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 13. RIZIKA
    # ═══════════════════════════════════════════════════════════
    story.append(p('13. Rizika implementace', 'h1'))
    story.append(hr())
    risk_rows = [
        ['API zmeny u CSU/Eurostatu', 'Stredni', 'Vysoky', 'Verzovani, fallback na CSV'],
        ['Kvalita dat (chybejici, revize)', 'Vysoka', 'Stredni', 'Validacni pipeline'],
        ['AI halucinace v komentarich', 'Stredni', 'Vysoky', 'Human-in-the-loop'],
        ['Kapacita tymu pro udrzbu', 'Vysoka', 'Vysoky', 'Max automatizace, dokumentace'],
        ['Bezpecnost (interni data)', 'Nizka', 'Kriticky', 'Separace verejne/interni'],
        ['Adopce uzivateli', 'Stredni', 'Vysoky', 'Zapojeni od zacatku, iterace'],
        ['Licencni naklady', 'Stredni', 'Stredni', 'Zacit s free zdroji'],
        ['GDPR / data governance', 'Nizka', 'Vysoky', 'Zadna PII v 1. fazi'],
        ['Scope creep', 'Vysoka', 'Stredni', 'Jasne faze, MVP pristup'],
    ]
    story.append(make_table(['Riziko', 'Pravdepodobnost', 'Dopad', 'Mitigace'], risk_rows,
                            col_widths=[avail_w*0.30, avail_w*0.17, avail_w*0.13, avail_w*0.40]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 14. ROADMAP
    # ═══════════════════════════════════════════════════════════
    story.append(p('14. Roadmap a prioritizace', 'h1'))
    story.append(hr())

    phases = [
        ('Faze 0: Quick wins', 'Dny', '#0d6efd', 'Quick win',
         'YoY toggle, Drill-down, Fullscreen, Print CSS, Sparkline, Hash routing, RSS monitoring'),
        ('Faze 1: Data Pipeline', '4-6 tydnu', '#ea580c', 'Build',
         'CSU API, Eurostat API, ECB/CNB, Transformace, Validace, GitHub Actions, Error handling'),
        ('Faze 2: Export + alerty', '3-4 tydny', '#ea580c', 'Build',
         'PDF export, PPTX generator, Excel export, Email/Slack notifikace, Anomalie detection'),
        ('Faze 3: News + foresighting', '2-3 tydny', '#ea580c', 'Build',
         'NewsAPI integrace, Deduplikace, Signpost tracking, Historicke srovnani'),
        ('Faze 4: AI funkce', '4-6 tydnu', '#7c3aed', 'Discovery -> Build',
         'Claude API testovani, AI komentare, AI klasifikace zprav, Review UI'),
        ('Faze 5: Multi-sector', '4-6 tydnu/sektor', '#ea580c', 'Build',
         'Refaktoring data modelu, Energetika, Stavebnictvi, Cross-sector dashboard'),
        ('Faze 6: Produkcni nasazeni', '6-8 tydnu', '#7c3aed', 'Discovery -> Build',
         'Interni infrastruktura, Security review, GDPR, AD/SSO, Interni data'),
        ('Faze 7: Advanced analytics', 'Prubezne', '#7c3aed', 'Discovery',
         'ML modely, Stress testing, Early warning, Monte Carlo, What-if'),
    ]

    for phase_name, duration, color, tag, items in phases:
        phase_box = Table([[
            Paragraph(f'<font color="{color}"><b>{phase_name}</b></font>&nbsp;&nbsp;'
                      f'<font size="8" color="#64748b">({duration})</font>',
                      ParagraphStyle('Phase', fontSize=11, leading=15, textColor=CS_DARK,
                                     fontName='Helvetica-Bold')),
        ]], colWidths=[avail_w])
        phase_box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor(color + '11')),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 2, HexColor(color)),
        ]))
        story.append(phase_box)
        story.append(Paragraph(f'<font size="8" color="#64748b">{items}</font>', S['small']))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 15. METRIKY
    # ═══════════════════════════════════════════════════════════
    story.append(p('15. Metriky uspechu', 'h1'))
    story.append(hr())

    met_rows = [
        ['Cas pripravy reportu', '15-22 hod', '5-8 hod', '3-4 hod', '2-2.5 hod'],
        ['Frekvence aktualizace dat', 'Ctvrtletne', 'Mesicne (auto)', 'Mesicne (auto)', 'Tydne (auto)'],
        ['Pocet sledovanych metrik', '~10 (manualne)', '20+ (auto)', '30+ (auto)', '50+ (auto)'],
        ['Pokryti sektoru', '1 (automotive)', '1', '1', '3-5'],
        ['Aktivni uzivatele', '0', '3-5', '5-10', '20+'],
        ['Cas od udalosti po alert', 'Dny', 'Hodiny', 'Hodiny', 'Minuty'],
        ['Podil automatizace', '0 %', '60 %', '75 %', '90 %'],
    ]
    story.append(make_table(
        ['Metrika', 'Baseline', 'Faze 1', 'Faze 3', 'Faze 6'],
        met_rows,
        col_widths=[avail_w*0.30, avail_w*0.17, avail_w*0.17, avail_w*0.18, avail_w*0.18]
    ))

    story.append(Spacer(1, 16))

    # ═══════════════════════════════════════════════════════════
    # 16. DISCOVERY BACKLOG
    # ═══════════════════════════════════════════════════════════
    story.append(p('16. Discovery backlog', 'h1'))
    story.append(hr())
    story.append(p('Vysoka priorita (overit v Fazi 1-2)', 'h2'))
    disc_high = [
        ['D1', 'Ma CS pristup k Bloomberg/Reuters API?', 'Treasury / IT', 'Pred Fazi 4'],
        ['D2', 'Existuje brand book / PPTX sablona CS?', 'Marketing / PR', 'Pred Fazi 2'],
        ['D3', 'Kdo bude realne platformu pouzivat?', 'Management', 'ASAP'],
        ['D4', 'Jake existujici nastroje tym pouziva?', 'Analyticky tym', 'ASAP'],
        ['D5', 'Budget pro AI API a datove licence?', 'Management', 'Pred Fazi 4'],
    ]
    story.append(make_table(['#', 'Otazka', 'Koho se zeptat', 'Deadline'], disc_high,
                            col_widths=[avail_w*0.06, avail_w*0.44, avail_w*0.25, avail_w*0.25]))

    story.append(Spacer(1, 8))
    story.append(p('Stredni priorita (overit v Fazi 3-4)', 'h2'))
    disc_mid = [
        ['D6', 'ACEA - povoduji scraping? Alternativni zdroj?', 'Legal / ACEA', 'Pred Fazi 1'],
        ['D7', 'Interni infrastruktura pro hosting?', 'IT oddeleni', 'Pred Fazi 6'],
        ['D8', 'GDPR posouzeni pro klientska data', 'Legal / DPO', 'Pred Fazi 6'],
        ['D9', 'AD/SSO integrace - technicke moznosti?', 'IT Security', 'Pred Fazi 6'],
        ['D10', 'Ma CS Teams nebo Slack? Webhook?', 'IT / komunikace', 'Pred Fazi 2'],
    ]
    story.append(make_table(['#', 'Otazka', 'Koho se zeptat', 'Deadline'], disc_mid,
                            col_widths=[avail_w*0.06, avail_w*0.44, avail_w*0.25, avail_w*0.25]))

    story.append(Spacer(1, 8))
    story.append(p('Nizsi priorita (overit v Fazi 5+)', 'h2'))
    disc_low = [
        ['D11', 'Propojeni s risk modely (PD, LGD, stress testy)', 'Risk oddeleni', 'Pred Fazi 7'],
        ['D12', 'CRM data pro klientsky profil x sektor', 'CRM tym', 'Pred Fazi 6'],
        ['D13', 'Cross-sector: jake sektory prioritizovat?', 'Management', 'Pred Fazi 5'],
        ['D14', 'Expert panel pro validaci scenaru?', 'Management', 'Pred Fazi 4'],
        ['D15', 'NLP pro ceske texty - kvalita, modely?', 'AI/ML tym', 'Pred Fazi 7'],
    ]
    story.append(make_table(['#', 'Otazka', 'Koho se zeptat', 'Deadline'], disc_low,
                            col_widths=[avail_w*0.06, avail_w*0.44, avail_w*0.25, avail_w*0.25]))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════
    # 17. PRINCIPY
    # ═══════════════════════════════════════════════════════════
    story.append(p('17. Principy implementace', 'h1'))
    story.append(hr())

    story.append(p('Co funguje dobre (lessons learned z prototypu):', 'h2'))
    for item in [
        '<b>Staticky web bez build stepu</b> — rychly vyvoj, snadny deploy na GitHub Pages',
        '<b>Chart.js</b> — dostatecne flexibilni pro vsechny typy grafu',
        '<b>Tailwind CSS via CDN</b> — rychle styling bez toolchainu',
        '<b>Oddeleni dat od logiky od layoutu</b> — cista architektura pro automatickou aktualizaci',
    ]:
        story.append(Paragraph(f'&bull;&nbsp;{item}', S['bullet']))

    story.append(Spacer(1, 10))
    story.append(p('Principy pro dalsi vyvoj:', 'h2'))

    principles = [
        ('MVP first', 'Kazda faze doda fungujici produkt, ne prototyp'),
        ('Automate everything', 'Pokud to lze automatizovat, automatizovat'),
        ('Human-in-the-loop pro AI', 'Nikdy nepublikovat AI vystup bez lidske revize'),
        ('Start with free data', 'Placene licence az po prokazani hodnoty'),
        ('Measure adoption', 'Sledovat, zda to nekdo pouziva, nez pridame dalsi funkce'),
        ('Keep it simple', 'Odolat scope creep, rikat "ne" nice-to-have'),
    ]
    for title, desc in principles:
        box = Table([[
            Paragraph(f'<b>{title}</b><br/><font size="8" color="#64748b">{desc}</font>',
                      ParagraphStyle('Principle', fontSize=10, leading=14, textColor=CS_BLUE,
                                     fontName='Helvetica-Bold'))
        ]], colWidths=[avail_w])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), CS_LIGHT_BLUE),
            ('ROUNDEDCORNERS', [6,6,6,6]),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(box)
        story.append(Spacer(1, 4))

    # ═══════════════════════════════════════════════════════════
    # BUILD
    # ═══════════════════════════════════════════════════════════
    doc.build(story, onFirstPage=title_page_bg, onLaterPages=normal_page_bg)
    print(f'PDF generated: {OUTPUT_PATH}')

if __name__ == '__main__':
    build_pdf()
