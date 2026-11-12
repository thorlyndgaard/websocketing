"""Exercício 9: exemplo de eco e chat usando WebSocket e Tornado."""

import json
import os

import tornado.ioloop
import tornado.web
import tornado.websocket


PORTA = int(os.environ.get("PORTA", "8887"))
PASTA = os.path.dirname(__file__)

# O histórico fica apenas na memória; reiniciar o programa apaga as mensagens.
conectados = set()
historico = []


class Pagina(tornado.web.RequestHandler):
    def initialize(self, nome):
        self.nome = nome

    def get(self):
        self.render(os.path.join(PASTA, self.nome))


class Repete(tornado.websocket.WebSocketHandler):
    def on_message(self, mensagem):
        # Responde somente ao navegador que enviou a mensagem.
        self.write_message(f"Servidor repete: {mensagem}")


class Chat(tornado.websocket.WebSocketHandler):
    def open(self):
        # Cada aba aberta tem uma conexão própria.
        conectados.add(self)
        for mensagem in historico:
            self.write_message(mensagem)

    def on_message(self, mensagem):
        try:
            dados = json.loads(mensagem)
            nome = dados["nome"].strip()
            texto = dados["texto"].strip()
            if not nome or not texto:
                return
        except (ValueError, KeyError, TypeError, AttributeError):
            return

        # Guarda até 50 mensagens e envia a nova para todas as abas.
        mensagem_pronta = json.dumps({"nome": nome[:30], "texto": texto[:500]})
        historico.append(mensagem_pronta)
        del historico[:-50]
        for cliente in tuple(conectados):
            cliente.write_message(mensagem_pronta)

    def on_close(self):
        conectados.discard(self)


def criar_app():
    return tornado.web.Application(
        [
            (r"/", tornado.web.RedirectHandler, {"url": "/repete"}),
            (r"/repete", Pagina, {"nome": "repete.html"}),
            (r"/chat", Pagina, {"nome": "chat.html"}),
            (r"/ws/repete", Repete),
            (r"/ws/chat", Chat),
        ]
    )


if __name__ == "__main__":
    # Escuta a rede local para permitir o teste com colegas na mesma rede.
    criar_app().listen(PORTA, address="0.0.0.0")
    print(f"Abra http://localhost:{PORTA}/repete ou http://localhost:{PORTA}/chat")
    tornado.ioloop.IOLoop.current().start()
