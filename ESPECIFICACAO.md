# Especificação das cartas

Tudo o que é preciso para gerar as artes e manter as cartas consistentes. O layout já está implementado em `ferramentas/gerar_pdf.py`; esta página descreve o que o script faz e como produzir as artes.

## 1. Formato

- **Tamanho:** 63 x 88 mm, retrato (mesmo tamanho de Magic e One Piece).
- **Resolução de referência:** 300 dpi, ou seja, 744 x 1039 px (1 mm = 11,81 px).
- **Sem full art:** a arte fica dentro de uma janela emoldurada, como nos TCGs clássicos.
- **Sem caixa de texto:** o espaço que seria da descrição vai para a arte e para as faixas de ícones.
- **Verso:** não é impresso. Dentro do sleeve vai o papel na frente e uma carta comum atrás.

## 2. Esboço

```
+-------------------------------------+
| +---------------------------------+ |
| | DRAGÃO BRASA                (C) | |  barra do nome + coroa
| +---------------------------------+ |
| +---------------------------------+ |
| |                                 | |
| |                                 | |
| |         JANELA DA ARTE          | |
| |                                 | |
| |                                 | |
| +---------------------------------+ |
| +---------------------------------+ |
| | E E E E                    (4)  | |  faixa de ataque
| +---------------------------------+ |
| +---------------------------------+ |
| | S S                        (2)  | |  faixa de defesa
| +---------------------------------+ |
|                              VUL 02 |
+-------------------------------------+
E = ícone de espada   S = ícone de escudo   (C) = selo da coroa
```

## 3. Medidas

Origem no canto superior esquerdo. A carta tem 63 x 88 mm. As posições abaixo são em mm.

| Elemento | Posição e tamanho |
|---|---|
| Nome | Começa em x 6,2, centralizado em y 8,2. Tem até 42 mm de largura com coroa e 50 mm nas demais cartas. |
| Selo da coroa | No canto direito da barra do nome, com cerca de 8 mm. Aparece nas cartas com 4 ou 5 espadas. |
| Área da arte | Começa em x 4 e y 14,4. Tem 55 x 39 mm e cantos chanfrados de 1,8 mm. |
| Ataque e defesa | Fileiras centralizadas em y 60,4 e 73,3. A primeira figura começa em x 6,4 e as seguintes avançam de 8 em 8 mm. |
| Numerais | Centralizados nos círculos pintados, em x 52,8. |
| Código | Alinhado à direita em x 58,6, com a base em y 82,7. |

## 4. Cores

A borda usa a `cor_borda` do deck como base. Vulcão usa terracota (`#BD492B`) e Mar usa azul (`#246598`). As variações de tinta na borda deixam a pintura aparecer nas duas cores.

O interior é de pergaminho claro, com filetes retos. O ataque usa vermelho queimado e a defesa usa cinza-grafite em todos os decks. Os dígitos são claros e a coroa tem um selo dourado.

## 5. Ícones

- **Ataque:** espada diagonal com lâmina clara e punho de cobre.
- **Defesa:** escudo cinza com faixa central dourada.
- O fundo pintado, a espada, o escudo e a coroa ficam em `ferramentas/moldura/`. O gerador repete cada ícone conforme o valor da carta.
- Os ícones de cada fileira têm sempre o mesmo tamanho e espaçamento para a criança comparar as quantidades e contar com o dedo.

## 6. Tipografia

- **Nome:** Cinzel Bold em caixa alta, até 18 caracteres. Começa em 11 pt e pode reduzir até 6,5 pt.
- **Numerais e código:** Cinzel Bold, em 19 pt e 6 pt.

## 7. Fichas de vida

- Círculo de 25 mm de diâmetro.
- Fundo pergaminho #E9D9B0, borda de 1,5 mm na cor do deck.
- Coração #C0392B de 15 mm, centralizado, contorno #2B2118.
- 6 por deck (5 + 1 reserva).

---

## 8. Direção de arte

### 8.1 Estilo

- Pintura tradicional de fantasia dos anos 1990, como as cartas de TCG impressas naquela época.
- Guache, acrílica ou óleo sobre papel, com pinceladas visíveis e textura leve de papel.
- Paleta limitada, de 4 a 6 cores principais por arte, com cores vivas.
- Contornos com pequenas variações e imperfeições de quem pintou à mão.
- Fundo simples, pintado à mão, com pouco detalhe (céu, rochas, água, manchas de cor).
- Uma fonte de luz principal, sombras simples.
- Monstro centralizado e inteiro (ou da cintura para cima, se for grande), em pose de ação.
- **Não citar nomes de franquias** no prompt. Descreva o estilo em vez de pedir "estilo de jogo X".

### 8.2 Para não parecer IA

Evitar:
- Render 3D, CGI, aspecto de videogame moderno.
- Brilho plástico, pele lisa de aerógrafo, degradês perfeitos.
- Efeito HDR, contraste exagerado, cores neon.
- Fundo desfocado tipo foto (bokeh).
- Excesso de detalhes, partículas brilhantes, faíscas por toda parte.
- Simetria perfeita.
- Olhos brilhando (glow).
- Erros de anatomia: conferir número de patas, dedos, garras e olhos.

### 8.3 Conteúdo (público de 4 anos)

- Monstros com cara de valentes e bravos, nunca de assustadores.
- Sem sangue, feridas, caveiras, ossos, olhos vazios ou dentes exagerados.
- Sem cena de morte ou de alguém sendo atacado. O monstro aparece sozinho.
- Sem texto, letras, números, assinatura ou marca d'água dentro da arte.

---

## 9. Gerando as artes

### 9.1 Fluxo

Gere **só a arte** no gerador de imagem. Moldura, nome e ícones são montados pelo script. Motivos:
- Geradores de imagem costumam errar a quantidade de ícones e escrever o nome errado. Aqui a contagem é a regra do jogo.
- Eles geram em proporções fixas, diferentes de 63 x 88 mm.
- Com o script, todas as cartas ficam idênticas em layout.

Se o gerador devolver a carta inteira (1061 x 1482 px ou a mesma proporção), rode `python3 ferramentas/extrair_arte.py carta.png "VUL 02"` com o código da carta para recortar a janela e salvar a arte no deck.

Para manter o mesmo estilo em todas:
1. Gere todas na mesma conversa.
2. Gere a primeira, aprove e diga: "use exatamente este estilo de pintura, paleta e acabamento para as próximas".
3. Gere uma por vez e confira cada uma antes de seguir.

### 9.2 Prompt da arte

Troque `[ASSUNTO]` e `[FUNDO]` pelos campos `assunto` e `fundo` do `cartas.json` do deck (também listados no README de cada deck).

```
Ilustração original para uma carta de jogo de cartas colecionáveis.

Estilo: pintura tradicional de fantasia dos anos 1990, feita à mão em guache e acrílica
sobre papel, com pinceladas visíveis, textura leve de papel e paleta limitada de cores
vivas. Deve parecer arte impressa em uma carta antiga, não arte digital.

Assunto: [ASSUNTO].
Fundo: [FUNDO], simples, pintado à mão e com pouco detalhe.
Enquadramento: monstro inteiro, centralizado, ocupando cerca de 70% da imagem, com
margem livre em cima e embaixo, porque a imagem será recortada. Formato quadrado.

Tom: valente e cheio de energia, adequado para uma criança de 4 anos. Sem sangue,
feridas, caveiras, ossos, olhos vazios, dentes exagerados ou expressão de terror.

Não incluir: texto, letras, números, moldura, borda, ícones, assinatura ou marca d'água.
Evitar: render 3D, CGI, brilho plástico, acabamento liso de aerógrafo, efeito HDR,
fundo desfocado de foto, excesso de partículas brilhantes, simetria perfeita e olhos
brilhando. Não imitar personagens nem artes de franquias existentes.
```

### 9.3 Arquivo da arte

- Formato quadrado, de preferência 1024 x 1024 ou maior, em PNG.
- O script recorta para a proporção da janela (55 x 39 mm), preservando mais do alto da imagem, então deixe o monstro centralizado com folga em cima e embaixo.
- Salve com o nome indicado no `cartas.json`, dentro de `decks/<deck>/arte/`.

---

## 10. Checklist antes de imprimir

- [ ] Todas as artes no lugar (o script lista as que faltam).
- [ ] Nada assustador ou violento nas artes.
- [ ] Artes sem texto, assinatura ou marca d'água.
- [ ] Anatomia conferida (patas, olhos, dedos).
- [ ] PDF gerado de novo depois de adicionar as artes.
- [ ] Impressão em 100%, com tamanho conferido contra uma carta real.
