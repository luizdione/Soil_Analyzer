"""Laudo de solo sintético em PDF, no formato da PESAGRO-RIO (cabeçalho em duas linhas, células mescladas).

Os números de solo reproduzem um laudo real de 4 amostras; siglas, laboratório e texto são fictícios.
Usado pelos testes para exercitar a leitura de PDF sem depender de um laudo de verdade.
"""
from __future__ import annotations

import io

CAB1 = ["Identificação da Amostra", "Prof. (cm)", "Textura (Expedita)", "pH em água", "M.O. g Kg-1",
        "cmol dm3 c", "", "", "", "", "", "", "", "", "%", "", "mg dm3", ""]
CAB2 = ["Registro no Laboratório", "", "", "", "", "K", "Ca", "Mg", "Al", "H +Al", "Na", "SB", "t", "T",
        "V", "m", "P", "K"]
AMOSTRAS = [
    ["1 – T15", "0 – 20", "Média", "5,00", "33,80", "0,08", "2,92", "2,73", "0,2", "2,60", "0,10", "5,83", "6,03",
     "8,43", "69", "3,32", "4", "31"],
    ["2 – T815", "0 – 20", "Média", "5,10", "26,70", "0,14", "2,09", "1,10", "0,2", "2,70", "0,06", "3,38", "3,58",
     "6,08", "56", "5,58", "22", "54"],
    ["3 – T17", "0 – 20", "Média", "5,43", "31,40", "0,19", "2,56", "1,88", "0,1", "2,00", "0,05", "4,68", "4,78",
     "6,68", "70", "2,09", "17", "74"],
    ["4 – T45", "0 – 20", "Média", "6,10", "39,42", "0,10", "3,29", "3,05", "0", "1,80", "0,03", "6,47", "6,47",
     "8,27", "78", "0,00", "18", "40"],
]
DATA = "23/09/2026"


def laudo_pdf() -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    estilos = getSampleStyleSheet()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=1 * cm, rightMargin=1 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.2 * cm)
    tabela = Table([CAB1, CAB2, *AMOSTRAS], repeatRows=2)
    tabela.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        *[("SPAN", (j, 0), (j, 1)) for j in range(1, 5)],
        ("SPAN", (5, 0), (13, 0)), ("SPAN", (14, 0), (15, 0)), ("SPAN", (16, 0), (17, 0)),
    ]))
    doc.build([
        Paragraph("LAUDO DE ANÁLISE DE SOLO — exemplo sintético no formato PESAGRO-RIO", estilos["Title"]),
        Paragraph(f"Laboratório de Solos (fictício) · Data: {DATA} · Amostras de 0 a 20 cm", estilos["Normal"]),
        Spacer(1, 12), tabela,
    ])
    return buf.getvalue()


if __name__ == "__main__":
    from pathlib import Path
    Path("laudo_sintetico.pdf").write_bytes(laudo_pdf())
    print("laudo_sintetico.pdf gravado")
