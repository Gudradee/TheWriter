#!/usr/bin/env python3
"""Gera as fichas do catálogo (Markdown) e a cópia do catálogo usada pelo painel.

Fonte única: data/catalogo.json
Saídas:
  skills/the-writer/references/catalogo/{autores,veiculos,tons,referencias}.md
  docs/catalogo.json e docs/catalogo.js (usado pelo painel)
  dist/the-writer.zip  (pacote para enviar no Claude.ai)

Uso: python3 scripts/build.py
"""
import json
import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "data" / "catalogo.json"
SKILL = RAIZ / "skills" / "the-writer"
SAIDA_MD = SKILL / "references" / "catalogo"
CAMADAS = ["autores", "veiculos", "tons", "referencias"]


def validar(cat):
    ids = {}
    erros = []
    for camada in CAMADAS:
        for grupo in cat[camada]["grupos"]:
            for item in grupo["itens"]:
                if item["id"] in ids:
                    erros.append(f"id duplicado: {item['id']}")
                ids[item["id"]] = camada
                for campo in ("nome", "resumo", "tecnicas", "evitar"):
                    if not item.get(campo):
                        erros.append(f"{item['id']}: campo vazio '{campo}'")
    esperado = {"principal": "autores", "secundarios": "autores", "veiculo": "veiculos", "tons": "tons", "jogadas": "referencias"}
    for mod in cat["modulos"]:
        if mod["id"] != "livre" and not (SKILL / "references" / "modulos" / f"{mod['id']}.md").exists():
            erros.append(f"módulo sem arquivo: {mod['id']}")
        if not mod["preset"]:
            continue
        for campo, camada in esperado.items():
            valores = mod["preset"][campo]
            for v in valores if isinstance(valores, list) else [valores]:
                if ids.get(v) != camada:
                    erros.append(f"preset {mod['id']}.{campo}: '{v}' não existe em {camada}")
    return ids, erros


def gerar_md(cat):
    SAIDA_MD.mkdir(parents=True, exist_ok=True)
    for camada in CAMADAS:
        bloco = cat[camada]
        linhas = [
            f"# {bloco['titulo']}",
            "",
            f"Camada: **{bloco['camada']}**.",
            "",
            "Arquivo gerado a partir de `data/catalogo.json`. Não edite à mão: edite o JSON e rode `python3 scripts/build.py`.",
            "",
            "Para achar um item, procure o cabeçalho `### <id>`.",
            "",
        ]
        for grupo in bloco["grupos"]:
            linhas += [f"## {grupo['nome']}", ""]
            for item in grupo["itens"]:
                linhas += [
                    f"### {item['id']}",
                    f"**{item['nome']}**: {item['resumo']}",
                    "",
                    "Técnicas:",
                ]
                linhas += [f"- {t}" for t in item["tecnicas"]]
                linhas += ["", f"Evitar: {item['evitar']}", ""]
        (SAIDA_MD / f"{camada}.md").write_text("\n".join(linhas), encoding="utf-8")


def empacotar():
    dist = RAIZ / "dist"
    dist.mkdir(exist_ok=True)
    destino = dist / "the-writer.zip"
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for arq in sorted(SKILL.rglob("*")):
            if arq.is_file():
                z.write(arq, Path("the-writer") / arq.relative_to(SKILL))
    return destino


def main():
    cat = json.loads(FONTE.read_text(encoding="utf-8"))
    ids, erros = validar(cat)
    if erros:
        print("Erros no catálogo:\n  " + "\n  ".join(erros))
        sys.exit(1)
    gerar_md(cat)
    shutil.copyfile(FONTE, RAIZ / "docs" / "catalogo.json")
    refs = SKILL / "references"
    textos = {
        "antiIA": (refs / "anti-ia.md").read_text(encoding="utf-8"),
        "bases": {t: (refs / "modulos" / f"_base-{t}.md").read_text(encoding="utf-8") for t in ("carrossel", "materia")},
        "modulos": {m["id"]: (refs / "modulos" / f"{m['id']}.md").read_text(encoding="utf-8")
                    for m in cat["modulos"] if m["id"] != "livre"},
    }
    (RAIZ / "docs" / "catalogo.js").write_text(
        "window.CATALOGO = " + json.dumps(cat, ensure_ascii=False) + ";\n"
        + "window.TEXTOS = " + json.dumps(textos, ensure_ascii=False) + ";\n", encoding="utf-8")
    # versão do catálogo no painel: evita o navegador usar um catalogo.js antigo em cache
    import hashlib, re
    js = (RAIZ / "docs" / "catalogo.js").read_bytes()
    versao_js = hashlib.sha1(js).hexdigest()[:10]
    html_p = RAIZ / "docs" / "index.html"
    html = html_p.read_text(encoding="utf-8")
    html = re.sub(r'catalogo\.js(\?v=[A-Za-z0-9]+)?"', f'catalogo.js?v={versao_js}"', html)
    html_p.write_text(html, encoding="utf-8")
    zipado = empacotar()
    contagem = {c: sum(len(g["itens"]) for g in cat[c]["grupos"]) for c in CAMADAS}
    print("OK", contagem, f"total={len(ids)}", f"módulos={len(cat['modulos'])}", zipado.name)


if __name__ == "__main__":
    main()
