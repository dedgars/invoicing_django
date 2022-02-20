from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import timedelta

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-BoldItalic', 'DejaVuSerif-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Italic', 'DejaVuSerif-Italic.ttf'))
pdfmetrics.registerFontFamily('DejaVuSerif', normal='DejaVu', bold='DejaVu-Bold',
                              italic='DejaVu-Italic', boldItalic='DejaVu-BoldItalic')

FONT = "DejaVu"


def generate_pdf(self):
    DOC_NAME = f"pdfs/akts-{self.number}.pdf"
    doc = SimpleDocTemplate(DOC_NAME, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='text', alignment=TA_JUSTIFY, fontName=FONT, fontSize=10, leading=15))
    styles.add(ParagraphStyle(name='text-right', alignment=TA_RIGHT, fontName=FONT, fontSize=10))
    styles.add(ParagraphStyle(name='text-center', alignment=TA_CENTER, fontName=FONT, fontSize=10))
    styles.add(ParagraphStyle(name='title-center', alignment=TA_CENTER, fontName=FONT, fontSize=14))

    Story = [
        Paragraph(f"<b>Rēķins Nr. {self.number}</b>", styles['text']),
        Spacer(1, 5),
        Paragraph(f"Datums: {self.create_date.strftime('%d.%m.%Y.')}", styles['text']),
        Spacer(1, 15),
    ]

    # customer data table
    data = [
        ["Maksātājs:", self.customer.name],
        ["Adrese:", self.customer.address],
        ["Reģ. Nr.:", self.customer.registration],
        ["PVN Reģ. Nr.:", self.customer.vat],
            ]
    t = Table(data, colWidths=[1.5 * inch] + [None])
    t.hAlign = "LEFT"
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
                           ('FONTNAME', (0, 0), (-1, -0), 'DejaVu-Bold'),
                           ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
                           ]))

    Story.append(t)
    Story.append(Spacer(1, 15))

    # Table header
    data = [["Apraksts", "Skaits", "Cena EUR", "Summa EUR"]]
    # Table lines
    for line in self.lines.all():
        data.append(
            [
                line.item,
                "{:.0f}".format(float(line.amount)),
                "{:.2f}".format(float(line.price)),
                "{:.2f}".format(float(line.total()))
            ])

    data.append(["", "", "Kopā:", "{:.2f}".format(float(self.total()))])
    data.append(["", "", "PVN:", "{:.2f}".format(float(self.vat()))])
    data.append(["", "", "Apmaksai:", "{:.2f}".format(float(self.total_with_vat()))])

    t = Table(data, colWidths=[3*inch] + [None] + [None] + [None])
    t.hAlign = "LEFT"
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
                           ('INNERGRID', (0, 0), (-1, -4), 0.25, colors.black),
                           ('FONTNAME', (0, 0), (-1, -0), 'DejaVu-Bold'),
                           ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                           ('BOX', (0, 0), (-1, -4), 0.25, colors.black),
                           ]))

    Story.append(t)
    Story.append(Spacer(1, 15))

    Story.append(Paragraph(f' {self.num_to_words()}', styles['text']),)
    due_date = self.create_date + timedelta(days=self.due_time)
    Story.append(Paragraph(f"Apmaksas termiņš: {due_date.strftime('%d.%m.%Y.')}", styles['text']))


    doc.build(Story)
