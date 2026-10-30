# Billie Jean — Structural Analysis

Ensaio multimídia de análise estrutural de *Billie Jean* (Michael Jackson, 1982), por Solomon Von Herclestein — Yield · The Chronicles of Financial Markets.

## Estrutura

```
index.html                  ← site publicável (Cloudflare Pages); autocontido
ideia/                      ← tese, roteiro de vídeo, prompt e rascunho de thumbnail
raciocinio/                 ← como a análise foi construída + checklist de verificação
modelos-html/               ← versões do HTML, diagramas PNG e script gerador
```

## Deploy (Cloudflare Pages)
1. pages.cloudflare.com → Create project → Connect to Git → este repositório
2. Framework preset: None · Build command: vazio · Output directory: `/`
3. Deploy

`index.html` é cópia de `modelos-html/billie_jean_published.html`. Os diagramas estão embutidos em base64 e o áudio é sintetizado no navegador (Web Audio API).

## Diagramas
`modelos-html/diagramas/` contém os PNGs usados no site (rótulos em inglês). `modelos-html/scripts/generate_diagrams.py` gera uma versão equivalente com rótulos em português (`pip install Pillow && python generate_diagrams.py`); não é idêntica pixel a pixel aos PNGs publicados.

**Antes de divulgar, leia `raciocinio/verificar_antes_de_publicar.md`.**
