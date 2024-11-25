import json

class Produto:
    def __init__(self, nome: str = None, preco: float = None, quantidade: int = None) -> None:
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def dump(self):
        return json.dumps({
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
        })

    def load(self, data: dict):
        self.nome = data["nome"]
        self.preco = data["preco"]
        self.quantidade = data["quantidade"]

    def __str__(self) -> str:
        return f"{self.nome} - R${self.preco:.2f}"

class Pedido:
    
    def __init__(self,pedidos,data,hora) -> None:
        self.pedidos = pedidos
        self.data = data
        self.hora = hora
        
    def dump(self):
        return json.dumps({
            "pedidos": self.pedidos,
            "data": self.data,
            "hora": self.hora,
        })
        
    def load(self,data: dict):
        self.pedidos = data["pedidos"]
        self.data = data["data"]
        self.hora = data["hora"]    
        
produtos = {
    1: Produto("Coca-Cola", 5.00, 6),
    2: Produto("Pepsi", 4.00, 1),
    3: Produto("Guaraná", 3.00, 7),
    4: Produto("Fanta", 2.00, 4),
    5: Produto("Sprite", 1.00, 1),
}