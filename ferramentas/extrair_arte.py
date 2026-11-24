"""Recorta a janela de arte de uma carta inteira e salva no deck."""

import argparse
import json
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent


def destino_da_arte(codigo):
    for manifesto in sorted((RAIZ / "decks").glob("*/cartas.json")):
        deck = json.loads(manifesto.read_text(encoding="utf-8"))
        for carta in deck["cartas"]:
            if carta["codigo"] == codigo:
                return manifesto.parent / "arte" / carta["arte"]
    raise ValueError(f"Código de carta desconhecido: {codigo}")


def recortar(caminho):
    with Image.open(caminho) as imagem:
        escala_x = imagem.width / 1061
        escala_y = imagem.height / 1482
        if not 0.99 <= escala_x / escala_y <= 1.01:
            raise ValueError("A carta deve ter proporção 1061 x 1482 (tolerância de 1%).")
        caixa = (round(116 * escala_x), round(228 * escala_y),
                 round(944 * escala_x), round(958 * escala_y))
        return imagem.crop(caixa)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("carta", type=Path, help="PNG com a carta inteira")
    parser.add_argument("codigo", help='código entre aspas, por exemplo "VUL 02"')
    parser.add_argument("--forcar", action="store_true", help="substitui uma arte existente")
    args = parser.parse_args()

    try:
        destino = destino_da_arte(args.codigo)
        arte = recortar(args.carta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("wb" if args.forcar else "xb") as arquivo:
            arte.save(arquivo, format="PNG")
    except FileExistsError:
        parser.exit(1, f"A arte já existe: {destino.relative_to(RAIZ)}. Use --forcar para substituir.\n")
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Erro: {erro}\n")
    print(f"Arte salva: {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
