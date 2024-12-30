from typing import Tuple
from funcao_postgree.bd_postgree_pedido import BdPedido
from funcao_postgree.bd_postgree_pedido_produto import BdPedidoProduto

bd_pedido = BdPedido()
bd_pedido_produto = BdPedidoProduto()

def transformar_lista_str_em_lista_tuple(lista: list[str]) -> list[Tuple[str, int]]:
    lista_tuple = []
    for item in lista:
        item_split = item.split(", ")
        id = item_split[0].split(": ")[1]
        preco = float(item_split[2].split(": ")[1])
        qtd = int(item_split[3].split(": ")[1])
        lista_tuple.append((id, preco, qtd))
    
    return lista_tuple

def editar_status_pedido(id_pedido: str, status: str) -> bool:
    status = bd_pedido.editar_status(status, id_pedido)
    return status

def inserir_pedido(produtos: list[Tuple[int, float, int]], mesa: int, status: str) -> bool:
    list_pedidos_dict = []
    for pedido in produtos:
        list_pedidos_dict.append({"produto_id": pedido[0], "preco_pago": pedido[1], "quantidade": pedido[2]})
        
    status = bd_pedido_produto.inserir_pedido_com_produtos(list_pedidos_dict, mesa, status)
    return status
  
def transformar_lista_str_em_lista_tuple(lista: list[str]) -> list[Tuple[str, int]]:
    lista_tuple = []
    for item in lista:
        item_split = item.split(", ")
        id = item_split[0].split(": ")[1]
        preco = float(item_split[2].split(": ")[1])
        qtd = int(item_split[3].split(": ")[1])
        lista_tuple.append((id, preco, qtd))
    
    return lista_tuple

def get_utimos_1000_pedidos() -> list[str]:
    pedidos = []
    for pedido in bd_pedido.get_last_1000():
        id = pedido[0]
        mesa = pedido[1]
        status = pedido[2]
        data_hora = pedido[3]
        pedidos.append(f"ID: {id}, Mesa: {mesa}, Status: {status}, Data/Hora: {data_hora}")
    
    return pedidos

def editar_status_pedido(id_pedido: str, status: str) -> bool:
    status = bd_pedido.editar_status(status, id_pedido)
    return status

def get_produtos_do_pedido(id_pedido: str) -> list[str]:
    pedidos = bd_pedido_produto.get_produtos_do_pedido(id_pedido)
    return pedidos