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

Origem (0, 0) no canto superior esquerdo da carta. Todas as medidas em mm.

| Elemento | Posição (x, y) | Tamanho | Detalhes |
|---|---|---|---|
| Borda externa | contorno da carta | 3 de espessura | Cor do deck. Filete de 0,5 na cor #2B2118 entre a borda e o fundo. |
| Fundo interno | 3, 3 | 57 x 82 | Pergaminho #E9D9B0. |
| Barra do nome | 5, 5 | 53 x 8 | Fundo #F4E8C8, contorno de 0,4 na cor #5A4630, cantos retos. |
| Nome | começa em x 7, centralizado na altura da barra | 9 pt (reduz até 6,5 pt se não couber) | Cinzel Bold, caixa alta, cor #2B2118, alinhado à esquerda. Largura máxima de 42 mm com coroa e 49 mm sem. |
| Selo da coroa | centro em 54, 9 | círculo de 6 | Só nos monstros com 4 ou 5 ⚔️. Fundo #D4A62A, contorno #5A4630, coroa #5A4630. |
| Janela da arte | 5, 15 | 53 x 47 | Moldura de 1 mm na cor #5A4630 e filete interno de 0,3 mm na cor #C9A86A. |
| Área da arte | 6, 16 | 51 x 45 | 602 x 531 px a 300 dpi. A arte preenche a área inteira. |
| Faixa de ataque | 5, 64 | 53 x 8 | Fundo #F3D0C4, contorno de 0,4 na cor #A0352A, cantos com raio de 2. |
| Faixa de defesa | 5, 73 | 53 x 8 | Fundo #D5DEE8, contorno de 0,4 na cor #4A5F78, cantos com raio de 2. |
| Ícones | começam em x 7, centralizados na altura da faixa | 6,5 cada, 1 de espaço entre eles | Quantidade igual ao valor, sempre alinhados à esquerda. Com 5 ícones, a fileira vai de x 7 a x 43,5. |
| Numeral | círculo com centro em x 53,75, na altura da faixa | círculo de 6,5 | Ataque com fundo #A0352A, defesa com fundo #4A5F78. Dígito branco em Fredoka Bold 11 pt. |
| Código | termina em x 58, base em y 84,3 | 5 pt | Ex.: "VUL 02". Fredoka Bold, cor #5A4630. Serve para organizar, não para jogar. |

## 4. Cores

| Uso | Cor |
|---|---|
| Borda do Deck Vulcão | #8B2E1F (bordô) |
| Borda do Deck Mar | #1F4E79 (azul marinho) |
| Fundo interno (pergaminho) | #E9D9B0 |
| Barra do nome | #F4E8C8 |
| Contornos e moldura | #5A4630 |
| Texto | #2B2118 |
| Faixa de ataque | fundo #F3D0C4, contorno e numeral #A0352A |
| Faixa de defesa | fundo #D5DEE8, contorno e numeral #4A5F78 |
| Coroa | #D4A62A |

## 5. Ícones

- **Espada (ataque):** espada simples na diagonal, ponta para cima e para a direita. Lâmina #C9CED6 com sulco #8E949C, guarda, cabo e pomo #A0352A, contorno #2B2B2B.
- **Escudo (defesa):** escudo clássico de ponta para baixo, visto de frente. Corpo #8A9BB0, faixa vertical central #E9D9B0, contorno #2B2B2B.
- **Estilo:** chapado, 2 ou 3 cores, contorno grosso, sem degradê e sem brilho. Reconhecível com 6,5 mm.
- **Regra de ouro:** mesmo tamanho e mesmo espaçamento em todas as cartas. É isso que permite comparar pelo comprimento da fileira.
- Os ícones são desenhados em vetor pelo script. Não usar emoji na carta impressa.

## 6. Tipografia

- **Nome:** Cinzel Bold.
- **Numerais e código:** Fredoka Bold.
- **Nomes curtos:** no máximo 18 caracteres.

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
- O script recorta no centro para a proporção da área da arte (51 x 45 mm), então deixe o monstro centralizado com folga em cima e embaixo.
- Salve com o nome indicado no `cartas.json`, dentro de `decks/<deck>/arte/`.

---

## 10. Checklist antes de imprimir

- [ ] Todas as artes no lugar (o script lista as que faltam).
- [ ] Nada assustador ou violento nas artes.
- [ ] Artes sem texto, assinatura ou marca d'água.
- [ ] Anatomia conferida (patas, olhos, dedos).
- [ ] PDF gerado de novo depois de adicionar as artes.
- [ ] Impressão em 100%, com tamanho conferido contra uma carta real.
