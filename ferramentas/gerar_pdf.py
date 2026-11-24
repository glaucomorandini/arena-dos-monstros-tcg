"""Gera o PDF de impressão da Arena dos Monstros.

Uso (na raiz do repositório):
    uv run --no-project --with reportlab --with pillow python3 ferramentas/gerar_pdf.py

Lê decks/*/cartas.json e as artes em decks/*/arte/.
Cartas sem arte saem com a janela da arte em branco e o aviso "ARTE PENDENTE".
Saída: impressao/arena-dos-monstros.pdf
"""

import json
import re
import sys
from functools import cache
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes"
MOLDURA = RAIZ / "ferramentas" / "moldura"
SAIDA = RAIZ / "impressao" / "arena-dos-monstros.pdf"
ORDEM_DECKS = ["vulcao", "mar"]

# Carta (mm)
CARTA_L, CARTA_A = 63, 88

# Cores
PERGAMINHO = HexColor("#E9D9B0")
MARROM = HexColor("#5A3825")
TEXTO = HexColor("#322014")
CORACAO = HexColor("#C0392B")
CORTE = HexColor("#888888")

# Folha A4
PAGINA_L, PAGINA_A = A4
COLUNAS, LINHAS = 3, 3
MARGEM_ESQ, MARGEM_TOPO = 10.5, 16.5

# Área interna da janela chanfrada (55 x 39 mm) a 300 dpi
ARTE_PX = (650, 461)


def registrar_fontes():
    pdfmetrics.registerFont(TTFont("Cinzel", str(FONTES / "Cinzel-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Fredoka", str(FONTES / "Fredoka-Bold.ttf")))


class Carta:
    """Desenha em coordenadas da carta: mm, origem no canto superior esquerdo."""

    def __init__(self, c, x0_mm, topo_mm):
        self.c = c
        self.x0 = x0_mm
        self.topo = topo_mm

    def X(self, x):
        return (self.x0 + x) * mm

    def Y(self, y):
        return PAGINA_A - (self.topo + y) * mm


def caminho(c, pontos, fechar=True):
    p = c.beginPath()
    p.moveTo(*pontos[0])
    for pt in pontos[1:]:
        p.lineTo(*pt)
    if fechar:
        p.close()
    return p


def icone_coracao(c, cx, cy, tam):
    s = tam
    c.saveState()
    c.translate(cx, cy)
    c.scale(s, s)
    p = c.beginPath()
    p.moveTo(0, -0.4)
    p.curveTo(-0.15, -0.25, -0.5, -0.05, -0.5, 0.15)
    p.curveTo(-0.5, 0.35, -0.35, 0.45, -0.2, 0.45)
    p.curveTo(-0.08, 0.45, 0, 0.38, 0, 0.28)
    p.curveTo(0, 0.38, 0.08, 0.45, 0.2, 0.45)
    p.curveTo(0.35, 0.45, 0.5, 0.35, 0.5, 0.15)
    p.curveTo(0.5, -0.05, 0.15, -0.25, 0, -0.4)
    p.close()
    c.setFillColor(CORACAO)
    c.setStrokeColor(TEXTO)
    c.setLineWidth(0.4 * mm / s)
    c.drawPath(p, fill=1, stroke=1)
    c.restoreState()


@cache
def preparar_arte(caminho_arte):
    """Enquadra a arte na janela a 300 dpi, preservando o alto dos monstros."""
    with Image.open(caminho_arte) as imagem:
        arte = ImageOps.fit(imagem.convert("RGB"), ARTE_PX, method=Image.Resampling.LANCZOS,
                            centering=(0.5, 0.08))
    return imagem_jpeg(arte)


@cache
def preparar_fundo(cor_borda):
    with Image.open(MOLDURA / "fundo.png") as pintura:
        fundo = Image.new("RGB", pintura.size, cor_borda)
        fundo.paste(pintura, mask=pintura.getchannel("A"))
    return imagem_jpeg(fundo)


def imagem_jpeg(img):
    jpeg = BytesIO()
    img.save(jpeg, format="JPEG", quality=90, subsampling=0)
    jpeg.seek(0)
    return ImageReader(jpeg)


def texto_ajustado(fonte, texto, tam, largura_max_mm, tam_min):
    while tam > tam_min and pdfmetrics.stringWidth(texto, fonte, tam) > largura_max_mm * mm:
        tam -= 0.25
    return tam


def desenhar_carta(c, x0, topo, carta, deck, pasta_deck):
    k = Carta(c, x0, topo)
    c.drawImage(preparar_fundo(deck["cor_borda"]), k.X(0), k.Y(CARTA_A),
                CARTA_L * mm, CARTA_A * mm)

    nome = carta["nome"].upper()
    coroa = carta["ataque"] >= 4
    tam = texto_ajustado("Cinzel", nome, 11, 42 if coroa else 50, 6.5)
    c.setFillColor(TEXTO)
    c.setFont("Cinzel", tam)
    c.drawString(k.X(6.2), k.Y(8.2) - tam * 0.35, nome)
    if coroa:
        c.drawImage(str(MOLDURA / "coroa.png"), k.X(49.6), k.Y(12.2),
                    8.7 * mm, 8 * mm, mask="auto")

    # A moldura pintada já contém o fundo da janela e os círculos dos números.
    arquivo = pasta_deck / "arte" / carta["arte"]
    if arquivo.exists():
        x, y, l, a, chanfro = 4.0, 14.4, 55.0, 39.0, 1.8
        vertices = [(x + chanfro, y), (x + l - chanfro, y), (x + l, y + chanfro),
                    (x + l, y + a - chanfro), (x + l - chanfro, y + a),
                    (x + chanfro, y + a), (x, y + a - chanfro), (x, y + chanfro)]
        c.saveState()
        c.clipPath(caminho(c, [(k.X(px), k.Y(py)) for px, py in vertices]), stroke=0)
        c.drawImage(preparar_arte(arquivo), k.X(x), k.Y(y + a), l * mm, a * mm)
        c.restoreState()
    else:
        c.setFillColor(HexColor("#FFF4D9"))
        c.setFont("Fredoka", 7)
        c.drawCentredString(k.X(31.5), k.Y(34), "ARTE PENDENTE")
        c.setFont("Fredoka", 5)
        c.drawCentredString(k.X(31.5), k.Y(38), carta["arte"])

    for valor, icone, centro_y in [(carta["ataque"], "espada", 60.4),
                                   (carta["defesa"], "escudo", 73.3)]:
        for i in range(valor):
            c.drawImage(str(MOLDURA / f"{icone}.png"), k.X(6.4 + 8.0 * i),
                        k.Y(centro_y + 4.6), 8.4 * mm, 9.2 * mm, mask="auto")
        c.setFillColor(HexColor("#FFF4D9"))
        c.setFont("Cinzel", 19)
        c.drawCentredString(k.X(52.8), k.Y(centro_y) - 19 * 0.35, str(valor))

    c.setFillColor(TEXTO)
    c.setFont("Cinzel", 6)
    c.drawRightString(k.X(58.6), k.Y(82.7), carta["codigo"])


def marcas_de_corte(c):
    c.setStrokeColor(CORTE)
    c.setLineWidth(0.2 * mm)
    xs = [MARGEM_ESQ + i * CARTA_L for i in range(COLUNAS + 1)]
    ys = [MARGEM_TOPO + j * CARTA_A for j in range(LINHAS + 1)]
    topo_grade, base_grade = ys[0], ys[-1]
    esq_grade, dir_grade = xs[0], xs[-1]
    for x in xs:
        c.line(x * mm, PAGINA_A - (topo_grade - 6) * mm, x * mm, PAGINA_A - (topo_grade - 2) * mm)
        c.line(x * mm, PAGINA_A - (base_grade + 2) * mm, x * mm, PAGINA_A - (base_grade + 6) * mm)
    for y in ys:
        c.line((esq_grade - 6) * mm, PAGINA_A - y * mm, (esq_grade - 2) * mm, PAGINA_A - y * mm)
        c.line((dir_grade + 2) * mm, PAGINA_A - y * mm, (dir_grade + 6) * mm, PAGINA_A - y * mm)


def rodape(c, texto):
    c.setFillColor(CORTE)
    c.setFont("Fredoka", 7)
    c.drawCentredString(PAGINA_L / 2, 5 * mm, texto)


def pagina_fichas(c, decks):
    c.setFillColor(TEXTO)
    c.setFont("Cinzel", 12)
    c.drawCentredString(PAGINA_L / 2, PAGINA_A - 20 * mm, "FICHAS DE VIDA")
    diam, espaco = 25, 5
    por_linha = 6
    largura = por_linha * diam + (por_linha - 1) * espaco
    x_ini = (210 - largura) / 2
    for j, (deck, _) in enumerate(decks):
        cor = HexColor(deck["cor_borda"])
        topo = 35 + j * (diam + 12)
        for i in range(por_linha):
            cx = x_ini + i * (diam + espaco) + diam / 2
            cy = topo + diam / 2
            c.setFillColor(PERGAMINHO)
            c.setStrokeColor(cor)
            c.setLineWidth(1.5 * mm)
            c.circle(cx * mm, PAGINA_A - cy * mm, (diam / 2 - 0.75) * mm, fill=1, stroke=1)
            icone_coracao(c, cx * mm, PAGINA_A - cy * mm, 15 * mm)
    rodape(c, "Arena dos Monstros  ·  recorte pela borda colorida  ·  imprimir em 100% (tamanho real)")


def carregar_decks():
    decks = []
    problemas = []
    codigos = set()
    for nome in ORDEM_DECKS:
        pasta = RAIZ / "decks" / nome
        deck = json.loads((pasta / "cartas.json").read_text(encoding="utf-8"))
        total = 0
        sigla = deck["sigla"]
        padrao = re.compile(rf"{re.escape(sigla)} (?:0[1-9]|[1-9][0-9])")
        for carta in deck["cartas"]:
            codigo = carta["codigo"]
            if codigo in codigos:
                problemas.append(f"{codigo}: código repetido")
            codigos.add(codigo)
            if not padrao.fullmatch(codigo):
                problemas.append(f"{codigo}: use {sigla} seguido de espaço e número de 01 a 99")
            if len(carta["nome"]) > 18:
                problemas.append(f"{codigo}: nome com mais de 18 caracteres")
            prefixo = codigo.replace(" ", "-") + "-"
            if not carta["arte"].startswith(prefixo):
                problemas.append(f"{codigo}: o nome do arquivo de arte deve começar com {prefixo}")
            a, d = carta["ataque"], carta["defesa"]
            if not (1 <= a <= 5 and 1 <= d <= 5):
                problemas.append(f"{carta['codigo']}: ataque e defesa precisam estar entre 1 e 5")
            if a + d != 6:
                problemas.append(f"{carta['codigo']}: ataque + defesa = {a + d}, deveria ser 6")
            total += carta["copias"]
        if total != 20:
            problemas.append(f"Deck {deck['deck']}: {total} cartas, deveria ter 20")
        decks.append((deck, pasta))
    return decks, problemas


def main():
    registrar_fontes()
    decks, problemas = carregar_decks()
    if problemas:
        print("Problemas nos decks:")
        for p in problemas:
            print("  " + p)
        sys.exit(1)

    fila = []
    pendentes = []
    for deck, pasta in decks:
        for carta in deck["cartas"]:
            if not (pasta / "arte" / carta["arte"]).exists():
                pendentes.append(f"decks/{pasta.name}/arte/{carta['arte']}")
            fila.extend([(carta, deck, pasta)] * carta["copias"])

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(SAIDA), pagesize=A4)
    c.setTitle("Arena dos Monstros")
    por_pagina = COLUNAS * LINHAS
    for inicio in range(0, len(fila), por_pagina):
        for i, (carta, deck, pasta) in enumerate(fila[inicio:inicio + por_pagina]):
            col, lin = i % COLUNAS, i // COLUNAS
            desenhar_carta(c, MARGEM_ESQ + col * CARTA_L, MARGEM_TOPO + lin * CARTA_A, carta, deck, pasta)
        marcas_de_corte(c)
        rodape(c, "Arena dos Monstros  ·  imprimir em 100% (tamanho real)  ·  cartas de 63 x 88 mm")
        c.showPage()
    pagina_fichas(c, decks)
    c.showPage()
    c.save()

    print(f"PDF gerado: {SAIDA.relative_to(RAIZ)} ({len(fila)} cartas)")
    if pendentes:
        print(f"{len(pendentes)} artes pendentes:")
        for p in pendentes:
            print("  " + p)

    sobrando = []
    for pasta_arte in (RAIZ / "decks").glob("*/arte"):
        manifesto = pasta_arte.parent / "cartas.json"
        cartas = json.loads(manifesto.read_text(encoding="utf-8"))["cartas"] if manifesto.exists() else []
        esperados = {pasta_arte / carta["arte"] for carta in cartas}
        sobrando.extend(p for p in pasta_arte.rglob("*")
                        if p.is_file() and p.name != ".gitkeep" and p not in esperados)
    if sobrando:
        print("Arquivos sobrando nas pastas de arte:")
        for p in sorted(sobrando):
            print(f"  {p.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
