"""Gera o PDF de impressão da Arena dos Monstros.

Uso (na raiz do repositório):
    pip install reportlab pillow
    python3 ferramentas/gerar_pdf.py

Lê decks/*/cartas.json e as artes em decks/*/arte/.
Cartas sem arte saem com a janela da arte em branco e o aviso "ARTE PENDENTE".
Saída: impressao/arena-dos-monstros.pdf
"""

import json
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes"
SAIDA = RAIZ / "impressao" / "arena-dos-monstros.pdf"
ORDEM_DECKS = ["vulcao", "mar"]

# Carta (mm)
CARTA_L, CARTA_A = 63, 88

# Cores
PERGAMINHO = HexColor("#E9D9B0")
BARRA_NOME = HexColor("#F4E8C8")
MARROM = HexColor("#5A4630")
TEXTO = HexColor("#2B2118")
CONTORNO_ICONE = HexColor("#2B2B2B")
ATQ_FUNDO = HexColor("#F3D0C4")
ATQ_COR = HexColor("#A0352A")
DEF_FUNDO = HexColor("#D5DEE8")
DEF_COR = HexColor("#4A5F78")
DOURADO = HexColor("#D4A62A")
LAMINA = HexColor("#C9CED6")
SULCO_LAMINA = HexColor("#8E949C")
ESCUDO = HexColor("#8A9BB0")
REALCE_ARTE = HexColor("#C9A86A")
ARTE_VAZIA = HexColor("#D8C9A0")
CORACAO = HexColor("#C0392B")
CORTE = HexColor("#888888")

# Folha A4
PAGINA_L, PAGINA_A = A4
COLUNAS, LINHAS = 3, 3
MARGEM_ESQ, MARGEM_TOPO = 10.5, 16.5

# Arte: área interna da janela (51 x 45 mm) a 300 dpi
ARTE_PX = (602, 531)


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

    def ret(self, x, y, l, a, preench=None, contorno=None, esp=0.0, raio=0):
        c = self.c
        if preench is not None:
            c.setFillColor(preench)
        if contorno is not None:
            c.setStrokeColor(contorno)
            c.setLineWidth(esp * mm)
        args = (self.X(x), self.Y(y + a), l * mm, a * mm)
        kw = dict(fill=1 if preench is not None else 0, stroke=1 if contorno is not None else 0)
        if raio:
            c.roundRect(*args, raio * mm, **kw)
        else:
            c.rect(*args, **kw)

    def circulo(self, cx, cy, r, preench=None, contorno=None, esp=0.0):
        c = self.c
        if preench is not None:
            c.setFillColor(preench)
        if contorno is not None:
            c.setStrokeColor(contorno)
            c.setLineWidth(esp * mm)
        c.circle(self.X(cx), self.Y(cy), r * mm,
                 fill=1 if preench is not None else 0,
                 stroke=1 if contorno is not None else 0)


def caminho(c, pontos, fechar=True):
    p = c.beginPath()
    p.moveTo(*pontos[0])
    for pt in pontos[1:]:
        p.lineTo(*pt)
    if fechar:
        p.close()
    return p


def icone_espada(c, cx, cy, tam):
    """Espada na diagonal, ponta para cima e para a direita. cx, cy e tam em pontos."""
    s = tam * 1.15
    c.saveState()
    c.translate(cx, cy)
    c.rotate(-45)
    c.scale(s, s)
    c.setLineWidth(0.3 * mm / s)
    c.setStrokeColor(CONTORNO_ICONE)
    c.setLineJoin(1)
    c.setFillColor(LAMINA)
    c.drawPath(caminho(c, [(-0.065, -0.12), (0.065, -0.12), (0.065, 0.34), (0, 0.48), (-0.065, 0.34)]),
               fill=1, stroke=1)
    c.setStrokeColor(SULCO_LAMINA)
    c.line(0, -0.08, 0, 0.32)
    c.setStrokeColor(CONTORNO_ICONE)
    c.setFillColor(ATQ_COR)
    c.rect(-0.04, -0.38, 0.08, 0.18, fill=1, stroke=1)
    c.rect(-0.22, -0.2, 0.44, 0.08, fill=1, stroke=1)
    c.circle(0, -0.42, 0.055, fill=1, stroke=1)
    c.restoreState()


def icone_escudo(c, cx, cy, tam):
    """Escudo de ponta para baixo com faixa central."""
    s = tam
    c.saveState()
    c.translate(cx, cy)
    c.scale(s, s)
    c.setLineWidth(0.3 * mm / s)
    c.setLineJoin(1)

    def contorno():
        p = c.beginPath()
        p.moveTo(-0.36, 0.42)
        p.lineTo(0.36, 0.42)
        p.lineTo(0.36, 0.05)
        p.curveTo(0.36, -0.2, 0.18, -0.36, 0, -0.46)
        p.curveTo(-0.18, -0.36, -0.36, -0.2, -0.36, 0.05)
        p.close()
        return p

    c.setFillColor(ESCUDO)
    c.drawPath(contorno(), fill=1, stroke=0)
    c.saveState()
    c.clipPath(contorno(), stroke=0, fill=0)
    c.setFillColor(PERGAMINHO)
    c.rect(-0.075, -0.5, 0.15, 1.0, fill=1, stroke=0)
    c.restoreState()
    c.setStrokeColor(CONTORNO_ICONE)
    c.drawPath(contorno(), fill=0, stroke=1)
    c.restoreState()


def icone_coroa(c, cx, cy, tam):
    s = tam
    c.saveState()
    c.translate(cx, cy)
    c.scale(s, s)
    c.setFillColor(MARROM)
    c.drawPath(caminho(c, [(-0.3, -0.16), (0.3, -0.16), (0.34, 0.18), (0.17, 0.03),
                           (0, 0.24), (-0.17, 0.03), (-0.34, 0.18)]), fill=1, stroke=0)
    c.rect(-0.3, -0.26, 0.6, 0.07, fill=1, stroke=0)
    for px, py in [(-0.34, 0.2), (0, 0.27), (0.34, 0.2)]:
        c.circle(px, py, 0.05, fill=1, stroke=0)
    c.restoreState()


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


def preparar_arte(caminho_arte):
    """Recorta no centro para a proporção da janela e reduz para 300 dpi."""
    img = Image.open(caminho_arte).convert("RGB")
    alvo = ARTE_PX[0] / ARTE_PX[1]
    l, a = img.size
    if l / a > alvo:
        nova_l = int(a * alvo)
        x = (l - nova_l) // 2
        img = img.crop((x, 0, x + nova_l, a))
    else:
        nova_a = int(l / alvo)
        y = (a - nova_a) // 2
        img = img.crop((0, y, l, y + nova_a))
    img = img.resize(ARTE_PX, Image.LANCZOS)
    return ImageReader(img)


def texto_ajustado(fonte, texto, tam, largura_max_mm, tam_min):
    while tam > tam_min and pdfmetrics.stringWidth(texto, fonte, tam) > largura_max_mm * mm:
        tam -= 0.25
    return tam


def desenhar_carta(c, x0, topo, carta, deck, pasta_deck):
    k = Carta(c, x0, topo)
    cor_deck = HexColor(deck["cor_borda"])
    coroa = carta["ataque"] >= 4

    # Borda e fundo
    k.ret(0, 0, CARTA_L, CARTA_A, preench=cor_deck)
    k.ret(3, 3, 57, 82, preench=PERGAMINHO, contorno=TEXTO, esp=0.5)

    # Barra do nome
    k.ret(5, 5, 53, 8, preench=BARRA_NOME, contorno=MARROM, esp=0.4)
    nome = carta["nome"].upper()
    larg_max = 42 if coroa else 49
    tam = texto_ajustado("Cinzel", nome, 9, larg_max, 6.5)
    c.setFillColor(TEXTO)
    c.setFont("Cinzel", tam)
    altura_maiuscula = tam * 0.7
    c.drawString(k.X(7), k.Y(9) - altura_maiuscula / 2, nome)

    if coroa:
        k.circulo(54, 9, 3, preench=DOURADO, contorno=MARROM, esp=0.3)
        icone_coroa(c, k.X(54), k.Y(9), 6 * mm)

    # Janela da arte
    k.ret(5, 15, 53, 47, preench=MARROM)
    caminho_arte = pasta_deck / "arte" / carta["arte"]
    if caminho_arte.exists():
        c.drawImage(preparar_arte(caminho_arte), k.X(6), k.Y(61), 51 * mm, 45 * mm)
    else:
        k.ret(6, 16, 51, 45, preench=ARTE_VAZIA)
        c.setFillColor(MARROM)
        c.setFont("Fredoka", 7)
        c.drawCentredString(k.X(31.5), k.Y(39), "ARTE PENDENTE")
        c.setFont("Fredoka", 5)
        c.drawCentredString(k.X(31.5), k.Y(43), carta["arte"])
    k.ret(6, 16, 51, 45, contorno=REALCE_ARTE, esp=0.3)

    # Faixas de ataque e defesa
    faixas = [
        (64, carta["ataque"], ATQ_FUNDO, ATQ_COR, icone_espada),
        (73, carta["defesa"], DEF_FUNDO, DEF_COR, icone_escudo),
    ]
    for y, valor, fundo, cor, icone in faixas:
        k.ret(5, y, 53, 8, preench=fundo, contorno=cor, esp=0.4, raio=2)
        cy = y + 4
        for i in range(valor):
            cx = 7 + i * 7.5 + 3.25
            icone(c, k.X(cx), k.Y(cy), 6.5 * mm)
        k.circulo(53.75, cy, 3.25, preench=cor)
        c.setFillColor(white)
        c.setFont("Fredoka", 11)
        c.drawCentredString(k.X(53.75), k.Y(cy) - 11 * 0.36, str(valor))

    # Código
    c.setFillColor(MARROM)
    c.setFont("Fredoka", 5)
    c.drawRightString(k.X(58), k.Y(84.3), carta["codigo"])


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
    for nome in ORDEM_DECKS:
        pasta = RAIZ / "decks" / nome
        deck = json.loads((pasta / "cartas.json").read_text(encoding="utf-8"))
        total = 0
        for carta in deck["cartas"]:
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


if __name__ == "__main__":
    main()
