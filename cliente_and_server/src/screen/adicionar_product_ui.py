from typing import Callable
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.func.func_produtos import inserir_produto
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao_server



class AdicionarProducto(QMainWindow):
    def __init__(self, atualizar_product: Callable):
        super().__init__()
        uic.loadUi('src/screen/ui/add_product.ui', self)
        
        self.pushButton_confim.clicked.connect(self.inserir_valor)
        self.pushButton_confim.clicked.connect(atualizar_product)
        
    def clear_values(self):
        self.lineEdit_nome.clear()
        self.lineEdit_preco.clear()
        self.comboBox_disponibilidade.setCurrentText("Disponível")

    def inserir_valor(self):
        try:
            nome = self.lineEdit_nome.text()
            preco = self.lineEdit_preco.text()
            status = self.comboBox_disponibilidade.currentText()

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")
            
            preco = float(preco)
            produto = {"nome": nome, "preco": preco, "disponivel": status == "Disponível"}

            if inserir_produto(produto):
                QMessageBox.information(self, "Sucesso", "Produto inserido com sucesso!")
                enviar_mensagem_de_sincronizacao_server("sync_produto")
                print("[LOG INFO] Produto inserido com sucesso!")
                self.clear_values()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
