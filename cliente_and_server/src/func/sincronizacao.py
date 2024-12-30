from typing import Callable

from sincronizacao_servidor_cliente import ClienteSincronizado, ServidorSincronizacao


cliente_sincronizado = ClienteSincronizado()
sync_server = ServidorSincronizacao()

def iniciar_cliente_sincronizado(on_mensage):
    cliente_sincronizado.iniciar(on_mensage)

def enviar_mensagem_de_sincronizacao_cliente(msg):
    cliente_sincronizado.enviar_mensagem(msg)

def iniciar_servidor_sincronizado(on_message: Callable):
    sync_server.iniciar(on_message)
    
def enviar_mensagem_de_sincronizacao_server(msg: str):
    sync_server.enviar_msg_para_todos_clientes(msg)

def close_server():
    enviar_mensagem_de_sincronizacao_server("server_down")
    sync_server.parar()
