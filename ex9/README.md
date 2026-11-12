# Exercício 9 — WebSocket

Este programa tem dois exemplos simples, baseados nas pastas `repete` e `chat` do repositório.

## Como executar

Na raiz do repositório:

```bash
python3 -m venv .venv
.venv/bin/pip install -r ex9/requirements.txt
.venv/bin/python ex9/server.py
```

No Windows, depois de criar o ambiente virtual, use `.venv\Scripts\pip install -r ex9/requirements.txt` e `.venv\Scripts\python ex9/server.py`.

Abra [http://localhost:8887/repete](http://localhost:8887/repete) e [http://localhost:8887/chat](http://localhost:8887/chat). Para o chat, abra duas abas e informe um nome diferente em cada uma.

Para o teste com colegas na mesma rede, o aluno que executa o servidor descobre o IP local e compartilha `http://IP_DO_SERVIDOR:8887/chat`. Os colegas abrem esse endereço no navegador. Se não conectar, confira a rede e a liberação da porta 8887 no firewall.

## Como funciona

- `server.py` entrega as páginas HTML e recebe conexões WebSocket.
- Em `/ws/repete`, o servidor devolve `Servidor repete: ...` apenas para quem enviou.
- Em `/ws/chat`, o servidor mantém um conjunto de conexões abertas. Quando chega uma mensagem, envia para todas elas. As últimas 50 mensagens ficam na memória para novas abas.
- O JavaScript abre a conexão usando o endereço da própria página, envia mensagens sem recarregar e exibe o que chega. A página do chat usa `textContent` para tratar as mensagens como texto.

## Resultados 

1. **Repete:** ao enviar `Olá`, a página mostra `Você disse: Olá` e depois `Servidor repete: Olá`. Outra aba não recebe essa resposta.
2. **Chat em duas abas:** uma mensagem enviada por uma aba aparece nas duas. Uma terceira aba recebe as últimas mensagens ao entrar.
3. **Chat com a turma:** descreva o teste real depois de executá-lo com os colegas, incluindo quais máquinas se conectaram e se as mensagens chegaram a todos.
