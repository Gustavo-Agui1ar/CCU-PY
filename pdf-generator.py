import csv
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# ======================
# CONFIGURAÇÕES
# ======================
PDF_ENTRADA = "pdfs/entrada.pdf"
PDF_OVERLAY = "pdfs/overlay.pdf"
PDF_SAIDA   = "pdfs/saida.pdf"
CSV_HORAS   = "results/horas.csv"

X_ENTRADA = 120
X_SAIDA   = 300

START_Y = 666
FONT_SIZE = 12
LINE_HEIGHT = FONT_SIZE * 1.21

# ======================
# 1. CRIAR OVERLAY
# ======================
c = canvas.Canvas(PDF_OVERLAY)
c.setFont("Helvetica", FONT_SIZE)

position_y = START_Y

with open(CSV_HORAS, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)

    next(reader)  # Pular cabeçalho

    for row in reader:
        dia, entrada, saida = row

        # Só escreve se houver horário
        if entrada.strip():
            c.drawString(X_ENTRADA, position_y, entrada)

        if saida.strip():
            c.drawString(X_SAIDA, position_y, saida)

        position_y -= LINE_HEIGHT

c.save()

# ======================
# 2. MESCLAR COM PDF ORIGINAL
# ======================
original = PdfReader(PDF_ENTRADA)
overlay = PdfReader(PDF_OVERLAY)

writer = PdfWriter()
page = original.pages[0]
page.merge_page(overlay.pages[0])
writer.add_page(page)

with open(PDF_SAIDA, "wb") as f:
    writer.write(f)
