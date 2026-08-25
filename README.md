# Daily Journal — Kit para Agentes

Ferramentas para agentes de IA consumirem o [Daily Journal](https://dailyjournal.news).

O Daily Journal é uma publicação que cobre notícias do mundo todo em português (pt-BR), com agregação de fontes (BBC, Financial Times, NYT, WSJ, Bloomberg, Al Jazeera, Folha, G1, UOL, CNN Brasil, etc.) e URLs canônicas para citação.

## Duas formas de conectar

| | [Servidor MCP](https://dailyjournal.news/mcp) | Plugin / skill (este repo) |
| --- | --- | --- |
| Onde funciona | Claude (web, desktop, Code), ChatGPT, Grok, qualquer cliente MCP | Claude Code |
| Instalação | Colar uma URL | Clonar o repo ou baixar o SKILL.md |
| Como o agente chama | Ferramentas nativas (`search_news`, `get_news`, `list_topics`, `get_topic`) | `curl` via Bash |
| Precisa de Bash | Não | Sim |

**Comece pelo servidor MCP.** É menos passos, funciona fora do Claude Code e não depende de acesso ao shell.

O plugin continua sendo a alternativa certa quando você quer o `curl` explícito no transcript, está montando um pipeline de shell em volta da API, ou trabalha num ambiente onde não dá para adicionar um conector.

## Servidor MCP

```bash
claude mcp add --transport http daily-journal https://dailyjournal.news/mcp
```

No Claude, ChatGPT ou Grok: Configurações → Conectores → adicionar conector personalizado → colar `https://dailyjournal.news/mcp`.

A página nessa mesma URL é o guia de instalação, em inglês e português. Sem autenticação, sem chave de API, todas as ferramentas somente leitura.

## Plugin para Claude Code

Clone o repo e aponte o Claude Code pra ele:

```bash
git clone https://github.com/daily-journal-tech/daily-journal-agents.git
claude --plugin-dir ./daily-journal-agents
```

O skill fica disponível como `daily-journal:daily-journal-api` e dispara automaticamente quando o usuário pergunta sobre notícias.

### Skill avulso

Se preferir instalar só o skill, sem a estrutura de plugin:

```bash
mkdir -p ~/.claude/skills/daily-journal-api
curl -fsSL https://raw.githubusercontent.com/daily-journal-tech/daily-journal-agents/main/skills/daily-journal-api/SKILL.md \
  -o ~/.claude/skills/daily-journal-api/SKILL.md
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

Documentação completa no [`SKILL.md`](skills/daily-journal-api/SKILL.md) ou em [dailyjournal.news/llms.txt](https://dailyjournal.news/llms.txt).

## Como citar

Quando seu agente usar dados do Daily Journal:

- **Linkar** `items[].url` (a página do DJ) ao parafrasear a síntese editorial
- **Linkar** `sources[].url` (URL externa do veículo original) ao citar reportagem direta
- **Atribuir** a marca do veículo por `outlets[].name` ("segundo a Folha de S.Paulo e o G1…")

## Privacidade

Política completa: [dailyjournal.news/privacidade](https://dailyjournal.news/privacidade).

O que se aplica especificamente a estas ferramentas:

- **Sem conta, sem chave.** Nem a API pública nem o servidor MCP pedem cadastro ou credencial, então nenhum dado de identificação é coletado no uso.
- **O que é registrado.** Requisições passam pelos logs de servidor padrão da nossa infraestrutura (endpoint, timestamp, user-agent, país derivado do IP), usados para operação e diagnóstico. Retenção de 24 horas.
- **O conteúdo das perguntas não chega até nós.** O agente traduz o pedido do usuário em parâmetros de busca; o texto da conversa fica no cliente.
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
