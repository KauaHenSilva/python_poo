from PyQt5.QtWidgets import QDialog, QLineEdit, QComboBox, QDialogButtonBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5 import uic
from src.func.func_pedido import get_produtos_do_pedido

class DialogoExibirProduto(QDialog):
    def __init__(self, id_pedido: int):
        super().__init__()
        uic.loadUi("src/screen/ui/exibir_pedido.ui", self) 
        self.prencher_campos(id_pedido)
        self.pushButton_exit.clicked.connect(self.accept)
    
    def prencher_campos(self, id_pedido: int):
        produtos = get_produtos_do_pedido(id_pedido)
        produtos_str = []
        for produto in produtos:
            pedido_atual_str = ''
            pedido_atual_str += f"Id: {produto['produto_id']}, "
            pedido_atual_str += f"nome: {produto['nome']}, "
            pedido_atual_str += f"quantidade: {produto['quantidade']}, "
            pedido_atual_str += f"preco pago na unidade: {produto['preco_pago']}"
            produtos_str.append(pedido_atual_str)
      
        model = QStandardItemModel()
        self.lst_todos_produtos_do_pedido.setModel(model)
        
        for pedido in produtos_str:
            item = QStandardItem(pedido)
            model.appendRow(item)