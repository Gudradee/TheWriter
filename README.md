<p align="center"><img src="docs/assets/logo.png" alt="the Writer" width="420"></p>

<p align="center">Skill para o Claude que escreve em português do Brasil a partir de um <b>perfil de escrita</b> montado por você.<br>Autor + veículo + tom + jogadas de referência, com módulos por área e revisão anti-IA.</p>

<p align="center"><a href="https://gudradee.github.io/TheWriter/"><b>Abrir o painel</b></a></p>

---

## A ideia

A maior parte do texto gerado por IA em português soa igual: "crucial", "jornada", "não é X, é Y", fecho otimista e nenhum fato. O the Writer resolve isso de dois jeitos:

1. **Perfis.** Em vez de "escreva um post", você monta uma combinação: *a metáfora de Shakespeare, com a estrutura do New York Times, em tom sério e informativo*. Cada camada traz técnicas concretas, descritas numa ficha.
2. **Regras.** A skill nunca inventa número, estudo, depoimento ou citação, respeita os limites de cada área (OAB, CFM, CVM, CDC/CONAR, TSE) e passa todo texto por uma revisão anti-IA feita para o português.

## O catálogo

| Camada | O que empresta | Itens |
|---|---|---|
| Autores | Linguagem e jeito de pensar | 54: fantasia, filósofos e especialistas, comunicação, jornalismo e digital, mulheres, especialistas de área |
| Veículos | Estrutura do texto | 29: sérios, comédia, drama, roteiro, digitais e mundiais, nicho |
| Tons | Postura diante do leitor | 25: informar, convencer, conectar, entreter, impressionar |
| Jogadas | Uma técnica de um trabalho consagrado | 22: de "Think Small" a "Snow Fall" |

Regra de mistura: 1 autor principal, até 2 secundários, 1 veículo, 1 ou 2 tons, até 2 jogadas.

## Módulos por área

| Carrossel | Matérias e textos |
|---|---|
| Finanças | Política |
| Saúde | Educação |
| Advocacia | Saúde |
| Marketing (genérico) | Ciência |

Cada módulo traz perfis prontos, referências da área, estrutura, limites legais e éticos, clichês proibidos e um checklist. Há também o modo **livre**, sem regras de área.

## Como usar

### 1. Instale a skill

**Claude Code**
```bash
git clone https://github.com/Gudradee/TheWriter.git
cp -r TheWriter/skills/the-writer ~/.claude/skills/
```

**Claude.ai / app do Claude**
Baixe [`dist/the-writer.zip`](dist/the-writer.zip) e envie nas configurações do Claude, na seção de skills.

**Outros agentes** (Codex, Cursor, Gemini CLI): copie a pasta `skills/the-writer` para a pasta de skills do agente.

### 2. Monte o perfil
Abra o [painel](https://gudradee.github.io/TheWriter/), escolha formato, autores, veículo, tom e jogadas, preencha o briefing e clique em **Copiar comando**.

### 3. Cole no Claude
O comando gerado tem este formato:
```
[the Writer · perfil]
modulo: carrossel-financas
principal: housel
secundarios:
veiculo: morning-brew
tons: didatico, conversa-de-bar
jogadas: two-young-men
canal: instagram
[briefing]
tema: por que o parcelado no cartão sai mais caro
publico: jovens no primeiro emprego
objetivo: educar e gerar salvamentos
fatos: ...
cta: salvar para consultar antes de comprar
```

Sem o painel também funciona: peça em linguagem natural ("escreve um carrossel de advocacia no estilo do Paul Graham, tom consultivo") ou só chame a skill, e ela abre um seletor na própria conversa.

## Estrutura do repositório

```
data/catalogo.json          fonte única do catálogo (edite aqui)
scripts/build.py            gera as fichas, o catálogo do painel e o zip
skills/the-writer/
  SKILL.md                  fluxo da skill
  references/
    anti-ia.md              revisão anti-IA para PT-BR
    catalogo/*.md           fichas geradas (autores, veículos, tons, referências)
    modulos/*.md            regras por área
docs/                       painel (GitHub Pages)
dist/the-writer.zip         pacote pronto para o Claude.ai
```

## Contribuir

Para adicionar um autor, veículo, tom ou jogada, edite `data/catalogo.json` (id, nome, resumo, 3 técnicas e o que evitar) e rode:

```bash
python3 scripts/build.py
```

O script valida ids e presets, gera as fichas e atualiza o painel e o zip.

## Sobre direitos autorais

A skill imita **técnicas**, nunca textos. Ela não reproduz trechos de obras, slogans ou bordões e não atribui frases inventadas a pessoas reais. Os nomes no catálogo servem como referência de estilo.

## Licença

MIT. Veja [LICENSE](LICENSE).
