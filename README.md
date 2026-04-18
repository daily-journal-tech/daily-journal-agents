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

- [`skills/daily-journal-api/`](skills/daily-journal-api/) — Skill/plugin para [Claude Code](https://claude.ai/code).
- _Em breve:_ servidor MCP, SDK JavaScript/Python, exemplos de integração.

## Instalação — Claude Code

### Plugin (recomendado)

Clone o repo e aponte o Claude Code pra ele:

```bash
git clone https://github.com/daily-journal-tech/daily-journal-agents.git
claude --plugin-dir ./daily-journal-agents
```

O skill fica disponível como `daily-journal:daily-journal-api` e dispara automaticamente quando o usuário pergunta sobre notícias brasileiras.

### Skill avulso

Se preferir instalar só o skill, sem a estrutura de plugin:

```bash
mkdir -p ~/.claude/skills/daily-journal-api
curl -fsSL https://raw.githubusercontent.com/daily-journal-tech/daily-journal-agents/main/skills/daily-journal-api/SKILL.md \
  -o ~/.claude/skills/daily-journal-api/SKILL.md
```

Na próxima sessão do Claude Code, o skill `daily-journal-api` é carregado automaticamente.

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

Documentação completa no [`SKILL.md`](skills/daily-journal-api/SKILL.md) ou em [dailyjournal.news/llms.txt](https://dailyjournal.news/llms.txt).

## Como citar

Quando seu agente usar dados do Daily Journal:

- **Linkar** `items[].url` (a página do DJ) ao parafrasear a síntese editorial
- **Linkar** `sources[].url` (URL externa do veículo original) ao citar reportagem direta
- **Atribuir** a marca do veículo por `outlets[].name` ("segundo a Folha de S.Paulo e o G1…")

## Licença

MIT. Ver [LICENSE](LICENSE).

---

Daily Journal · [dailyjournal.news](https://dailyjournal.news) · [@dailyjournal.news](https://www.instagram.com/dailyjournal.news)
