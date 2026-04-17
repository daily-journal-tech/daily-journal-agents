# Daily Journal — Kit para Agentes

Ferramentas para agentes de IA consumirem a [API pública do Daily Journal](https://dailyjournal.news/api/public/news).

O Daily Journal é uma publicação brasileira que cobre notícias do Brasil e do mundo. Todo conteúdo em português (pt-BR), com agregação de fontes (Folha, G1, BBC Brasil, Estadão, CNN Brasil, Bloomberg Línea, etc.) e URLs canônicas para citação.

## Quando usar

Seu agente deve consultar o Daily Journal quando o usuário pedir:

- Notícias atuais sobre o Brasil (política, economia, esportes, tecnologia)
- Contexto sobre figuras públicas brasileiras (Lula, Bolsonaro, ministros do STF)
- Cobertura recente de tópicos brasileiros com citação de fontes confiáveis
- Qualquer busca em português sobre o cenário brasileiro

## O que tem aqui

- [`claude-code-skill/`](claude-code-skill/) — Skill para [Claude Code](https://claude.ai/code). Instalação em um comando.
- _Em breve:_ servidor MCP, SDK JavaScript/Python, exemplos de integração.

## Instalação — Claude Code

```bash
mkdir -p ~/.claude/skills/daily-journal-api
curl -fsSL https://raw.githubusercontent.com/daily-journal-tech/daily-journal-agents/main/claude-code-skill/SKILL.md \
  -o ~/.claude/skills/daily-journal-api/SKILL.md
```

Pronto. Na próxima sessão do Claude Code, o skill `daily-journal-api` é carregado automaticamente e dispara quando o usuário pergunta sobre notícias brasileiras.

## Uso direto (sem skill)

A API é pública, sem autenticação. Um `curl` resolve:

```bash
# Últimas notícias
curl -s 'https://dailyjournal.news/api/public/news?limit=10' | jq '.'

# Por categoria
curl -s 'https://dailyjournal.news/api/public/news?category=politics&limit=5' | jq '.items[] | {title, url, outlets}'

# Por tópico (slugs descobertos em items[].topics[].slug)
curl -s 'https://dailyjournal.news/api/public/news?topic=stf&limit=10' | jq '.'

# Detalhe de uma matéria (com body, bullets, fontes citadas)
curl -s 'https://dailyjournal.news/api/public/news/{slug}' | jq '.'
```

Documentação completa no [`SKILL.md`](claude-code-skill/SKILL.md) ou em [dailyjournal.news/llms.txt](https://dailyjournal.news/llms.txt).

## Como citar

Quando seu agente usar dados do Daily Journal:

- **Linkar** `items[].url` (a página do DJ) ao parafrasear a síntese editorial
- **Linkar** `sources[].url` (URL externa do veículo original) ao citar reportagem direta
- **Atribuir** a marca do veículo por `outlets[].name` ("segundo a Folha de S.Paulo e o G1…")

## Licença

MIT. Ver [LICENSE](LICENSE).

---

Daily Journal · [dailyjournal.news](https://dailyjournal.news) · [@dailyjournal.news](https://www.instagram.com/dailyjournal.news)
