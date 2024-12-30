from typing import Tuple


pedidos_em_desenvolvimento: list[tuple[str, int]] = []

def adicionar_pedido_em_desenvolvimento(produto: str, qtd: int) -> Tuple[bool, str]:
    confirm = (True, "Pedido adicionado com sucesso")
    
    if "indisponível" in produto.split(", ")[3].split(": ")[1]:
        confirm = (False, "Produto indisponível")
        print("[LOG INFO] Produto indisponível")
        return confirm
    
    produto_split = produto.split(", ")[0:3]
    produto_split = ", ".join(produto_split)
    
    only_produto = [produto for produto, _ in pedidos_em_desenvolvimento]
    
    if produto_split in only_produto:
        index = only_produto.index(produto_split)
        pedidos_em_desenvolvimento[index] = (produto_split, qtd + pedidos_em_desenvolvimento[index][1])
    else:
        pedidos_em_desenvolvimento.append((produto_split, qtd))
    
    return confirm

def pegar_pedidos_em_desenvolvimento_str() -> list[str]:
    produtos =  [f"{produto}, Quantidade: {qtd}" for produto, qtd in pedidos_em_desenvolvimento]
    return sorted(produtos, key=lambda x: int(x.split(",")[0].split(": ")[1]))
    

def remover_pedido_em_desenvolvimento(pedido_em_desenvolvimento: str, qtd: int) -> Tuple[bool, str]:
    confirm = (True, "Pedido removido com sucesso")
    
    pegar_id = pedido_em_desenvolvimento.split(", ")[0].split(": ")[1]
    
    for produto, quantidade_disponivel in pedidos_em_desenvolvimento:
        id_produto = produto.split(", ")[0].split(": ")[1]
        
        if id_produto == pegar_id:
            
            if qtd == quantidade_disponivel:
                pedidos_em_desenvolvimento.remove((produto, quantidade_disponivel))
                print("[LOG INFO] Pedido removido")
            elif qtd < quantidade_disponivel:
                pedidos_em_desenvolvimento[pedidos_em_desenvolvimento.index((produto, quantidade_disponivel))] = (produto, quantidade_disponivel - qtd)
                print("[LOG INFO] Pedido decrementado")
            else:
                confirm = (False, "Quantidade maior que a disponível")
                print("[LOG INFO] Quantidade maior que a disponível")
                
            return confirm

    return (False, "Pedido não encontrado")

def finalizar_pedido_em_desenvolvimento() -> Tuple[bool, str]:
    confirm = (True, "Pedido finalizado com sucesso")
    
    if not pedidos_em_desenvolvimento:
        confirm = (False, "Nenhum pedido em desenvolvimento")
        print("[LOG INFO] Nenhum pedido em desenvolvimento")
        return confirm
    
    pedidos_em_desenvolvimento.clear()
    
    return confirm
