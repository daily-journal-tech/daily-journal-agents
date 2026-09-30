# Daily Journal — Kit para Agentes

Ferramentas para agentes de IA consumirem o [Daily Journal](https://dailyjournal.news).

O Daily Journal é uma publicação que cobre notícias do mundo todo em português (pt-BR), com agregação de fontes (BBC, Financial Times, NYT, WSJ, Bloomberg, Al Jazeera, Folha, G1, UOL, CNN Brasil, etc.) e URLs canônicas para citação.

## Duas formas de conectar

| | [Servidor MCP](https://dailyjournal.news/mcp) | Plugin (este repo) |
| --- | --- | --- |
| Onde funciona | Claude (web, desktop, Code), ChatGPT, Grok, qualquer cliente MCP | Claude (web, desktop, mobile), Cowork, Claude Code |
| Instalação | Colar uma URL | Diretório de plugins do Claude, ou clonar o repo |
| O que traz | As quatro ferramentas (`search_news`, `get_news`, `list_topics`, `get_topic`) | O mesmo servidor MCP, mais um skill que ensina o fluxo e a citação, e os comandos `/resumo` e `/topico` |

O plugin inclui o servidor MCP (`.mcp.json`), então não é preciso instalar os dois. No claude.ai e no Cowork, o conector aparece na aba **Connectors** do plugin; conecte por lá (sem login, sem chave). Fora do Claude, use o servidor MCP direto.

## Servidor MCP

```bash
claude mcp add --transport http daily-journal https://dailyjournal.news/mcp
```

No Claude, ChatGPT ou Grok: Configurações → Conectores → adicionar conector personalizado → colar `https://dailyjournal.news/mcp`.

A página nessa mesma URL é o guia de instalação, em inglês e português. Sem autenticação, sem chave de API, todas as ferramentas somente leitura.

Quatro ferramentas: `search_news`, `get_news`, `list_topics` e `get_topic`. As
páginas de tópico grandes voltam cortadas num orçamento de 25 mil caracteres,
porque `guerra-do-ira` sozinha tem ~170 mil. O índice completo das seções vem
sempre, e `sections_notice` diz qual chamada busca o que ficou de fora:
`sections: ["linha-do-tempo"]`, ou `section_offset` para continuar uma seção
maior que o orçamento.

## Plugin

No Claude: **Customize → Plugins → Discover**, procure "Daily Journal" e instale. Depois conecte o servidor na aba **Connectors** do plugin.

No Claude Code, a partir do repo:

```bash
git clone https://github.com/daily-journal-tech/daily-journal-agents.git
claude --plugin-dir ./daily-journal-agents
```

O que vem no plugin:

- **Servidor MCP** `daily-journal`: as quatro ferramentas.
- **Skill** `daily-journal-api`: quando usar cada ferramenta, como lidar com tópicos grandes e como citar. Dispara sozinho em perguntas sobre notícias do Brasil. Se as ferramentas não estiverem conectadas e houver shell, cai para `curl` na API pública ([`references/curl-api.md`](skills/daily-journal-api/references/curl-api.md)).
- **`/daily-journal:resumo [tema]`**: resumo do dia, com data, link e veículos de cada notícia.
- **`/daily-journal:topico <tema>`**: contexto de uma pessoa, instituição ou história em andamento, a partir da página de tópico.

### Skill avulso

Se preferir instalar só o skill, sem a estrutura de plugin (ele usa `curl`, então precisa de shell):

```bash
D=~/.claude/skills/daily-journal-api; R=https://raw.githubusercontent.com/daily-journal-tech/daily-journal-agents/main/skills/daily-journal-api
mkdir -p "$D/references"
curl -fsSL "$R/SKILL.md" -o "$D/SKILL.md"
curl -fsSL "$R/references/curl-api.md" -o "$D/references/curl-api.md"
```

Na próxima sessão do Claude Code, o skill `daily-journal-api` é carregado automaticamente.

## Exemplos de uso

Depois de instalar, por qualquer um dos caminhos:

**"O que aconteceu no STF esta semana?"**
O agente busca por tópico (`stf`) com filtro de data, devolve as manchetes com data e link, e cita os veículos que cobriram cada uma.

**"Me dá o contexto completo da guerra do Irã, com fontes."**
O agente abre a página de tópico, que traz resumo editorial, seções ordenadas, perguntas frequentes e as notícias recentes ligadas ao tema. Cada notícia vem com a URL do veículo original.

**"O que a imprensa brasileira e a internacional estão dizendo sobre as tarifas do Trump?"**
Busca full-text por `trump tarifas`, depois abre as matérias em detalhe para ler a lista completa de `sources[]` e comparar o que cada veículo publicou.

## Uso direto (sem MCP e sem skill)

A API é pública, sem autenticação. Um `curl` resolve:

```bash
# Últimas notícias
curl -s 'https://dailyjournal.news/api/public/news?limit=10' | jq '.'

# Por categoria
curl -s 'https://dailyjournal.news/api/public/news?category=world&limit=5' | jq '.items[] | {title, url, outlets}'

# Por tópico (slugs descobertos em items[].topics[].slug)
curl -s 'https://dailyjournal.news/api/public/news?topic=emmanuel-macron&limit=10' | jq '.'

# Busca full-text (combina com qualquer filtro)
curl -s 'https://dailyjournal.news/api/public/news?search=trump%20tariffs&limit=10' | jq '.'

# Detalhe de uma matéria (com body, bullets, fontes citadas)
curl -s 'https://dailyjournal.news/api/public/news/{slug}' | jq '.'

# Páginas de tópico (cobertura evergreen; filtra por category e hot)
curl -s 'https://dailyjournal.news/api/public/topics?limit=10' | jq '.'

# Detalhe de um tópico (com seções, perguntas frequentes e notícias recentes)
curl -s 'https://dailyjournal.news/api/public/topics/{slug}?news_limit=10' | jq '.'
```

Documentação completa em [`references/curl-api.md`](skills/daily-journal-api/references/curl-api.md) ou em [dailyjournal.news/llms.txt](https://dailyjournal.news/llms.txt).

## Como citar

Quando seu agente usar dados do Daily Journal:

- **Linkar** `items[].url` (a página do DJ) ao parafrasear a síntese editorial
- **Linkar** `sources[].url` (URL externa do veículo original) ao citar reportagem direta
- **Atribuir** a marca do veículo por `outlets[].name` ("segundo a Folha de S.Paulo e o G1…")

## Privacidade

Política completa: [dailyjournal.news/privacidade](https://dailyjournal.news/privacidade).

O que se aplica especificamente a estas ferramentas:

- **Sem conta, sem chave.** Nem a API pública nem o servidor MCP pedem cadastro ou credencial, então nenhum dado de identificação pessoal é coletado no uso.
- **O que é registrado.** Requisições passam pelos logs de servidor padrão da nossa infraestrutura (endpoint, timestamp, user-agent, país derivado do IP), usados para operação e diagnóstico, com retenção de 24 horas.
- **Métricas de uso do servidor MCP.** Cada conexão e cada chamada de ferramenta gera um evento anônimo na nossa ferramenta de análise (PostHog): nome e versão do cliente MCP, user-agent, a ferramenta chamada e os parâmetros de busca que o agente enviou (termo, categoria, tópico, slug, datas). Não há identificador de pessoa nem perfil de usuário. Usamos isso para saber quais agentes nos usam e o que procuram.
- **O conteúdo da conversa não chega até nós.** O agente traduz o pedido do usuário em parâmetros de busca; só esses parâmetros chegam, o texto da conversa fica no cliente.
- **Sem compartilhamento com terceiros** para publicidade ou perfilamento. Provedores de infraestrutura processam o tráfego apenas para entregá-lo.
- **Dados devolvidos são públicos.** É o mesmo conteúdo editorial publicado em dailyjournal.news.

## Segurança

Para reportar uma vulnerabilidade, veja [SECURITY.md](SECURITY.md).

## Suporte

Dúvidas, problemas ou sugestões: [oi@dailyjournal.com.br](mailto:oi@dailyjournal.com.br) ou uma [issue no repositório](https://github.com/daily-journal-tech/daily-journal-agents/issues).

## Licença

MIT. Ver [LICENSE](LICENSE).

---

Daily Journal · [dailyjournal.news](https://dailyjournal.news) · [@dailyjournal.news](https://www.instagram.com/dailyjournal.news)
