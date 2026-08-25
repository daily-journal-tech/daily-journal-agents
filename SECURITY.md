# Política de segurança

## Como reportar

Mande um e-mail para **[oi@dailyjournal.com.br](mailto:oi@dailyjournal.com.br)** com `[security]` no assunto. Não abra issue pública para vulnerabilidade.

Ajuda muito incluir:

- O que dá pra fazer com a falha, em uma frase.
- Passos para reproduzir, ou um `curl` que demonstre.
- Qual superfície: servidor MCP (`dailyjournal.news/mcp`), API pública (`dailyjournal.news/api/public/*`), o skill deste repo, ou o site.
- Se você quer crédito público pelo report, e sob qual nome.

## O que esperar

- **Confirmação de recebimento em até 5 dias úteis.**
- Uma avaliação inicial com o que concluímos e o que pretendemos fazer.
- Correção priorizada pelo impacto. Falhas exploráveis sem autenticação vêm primeiro.
- Aviso quando estiver corrigido.

Não temos programa de recompensa. Somos uma equipe pequena e respondemos como gente, não como formulário.

## Escopo

Dentro do escopo:

- Servidor MCP em `https://dailyjournal.news/mcp`
- API pública em `https://dailyjournal.news/api/public/*`
- O skill e o plugin deste repositório
- `https://dailyjournal.news`

Fora do escopo:

- Serviços de terceiros que hospedam ou entregam o site
- Ataques de negação de serviço e testes de carga
- Engenharia social contra a equipe ou contra leitores
- Relatórios que só apontam ausência de um header, sem impacto demonstrado

## Um ponto sobre o conteúdo

O Daily Journal agrega reportagem de outros veículos. Erro editorial, atribuição incorreta ou pedido de correção numa matéria **não é** questão de segurança: esse caminho é [oi@dailyjournal.com.br](mailto:oi@dailyjournal.com.br) sem o prefixo `[security]`, ou a página de [contato](https://dailyjournal.news/contact).

## Ao testar

A API e o servidor MCP são públicos, sem autenticação e somente leitura. Pode explorá-los à vontade dentro do razoável: cerca de 30 requisições por minuto. Não precisa de permissão prévia para ler dados públicos. Precisa, sim, para qualquer coisa que gere carga sustentada.
