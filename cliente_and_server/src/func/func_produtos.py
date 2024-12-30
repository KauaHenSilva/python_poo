from typing import Tuple, Union
import json
from funcao_postgree.bd_postgree_produto import BdProduto

bd_produto = BdProduto()


def inserir_produto(product: dict[str, Union[str, int, bool]]) -> bool:
    status = bd_produto.insert_produto(json.dumps(product))
    return status


def atualizar_produto(product: dict[str, Union[str, int, float]], id_product: str) -> bool:
    status = bd_produto.atualizar_produto(json.dumps(product), int(id_product))
    return status

def trocar_disponibilidade(id_product: str) -> bool:
    status = bd_produto.trocar_disponibilidade(id_product)
    return status


def remover_produto(id_product: str) -> bool:
    status = bd_produto.remover_produto(id_product)
    return status


def pegar_todos_itens_str() -> list[str]:
    produtos = []
    for product in bd_produto.get_all():
        id = product[0]
        nome = product[1]
        preco = product[2]
        disponivel = "disponível" if bool(product[3]) else "indisponível"
        produtos.append(f"ID: {id}, Nome: {nome}, Preço: {preco}, Status: {disponivel}")
    
    return produtos
  