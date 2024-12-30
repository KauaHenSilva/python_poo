from typing import Callable, Tuple
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from src.func.func_produtos import atualizar_produto
from src.func.sincronizacao import enviar_mensagem_de_sincronizacao_server


class EditarProduto(QMainWindow):
    def __init__(self, atualizar_product: Callable):
        super().__init__()
        uic.loadUi('src/screen/ui/editar_product.ui', self)
        self.pushButton_confim.clicked.connect(self.editar_valor)
        self.pushButton_confim.clicked.connect(atualizar_product)
      
    def start_values(self, values_start: Tuple[str, str, str, str]):
        self.id, nome, preco, disponivel = values_start
        self.label_id.setText(f"Id do pedido: {self.id}")
        self.lineEdit_nome.setText(nome)
        self.comboBox_disponibilidade.setCurrentText("Disponível" if disponivel == "disponível" else "Indisponível")
        self.lineEdit_preco.setText(preco)

    def editar_valor(self):
        try:
            nome = self.lineEdit_nome.text()
            preco = self.lineEdit_preco.text()
            disponivel = self.comboBox_disponibilidade.currentText()

            if not nome:
                raise ValueError("O nome do produto não pode estar vazio.")
            if not preco.replace('.', '', 1).isdigit():
                raise ValueError("O preço deve ser um número válido.")
            
            disponivel = disponivel == "Disponível"

            preco = float(preco)
            produto = {"nome": nome, "disponivel": disponivel, "preco": preco}
            
            if atualizar_produto(produto, self.id):
                QMessageBox.information(self, "Sucesso", "Produto editado!")
                enviar_mensagem_de_sincronizacao_server("sync_produto")
                print("[LOG INFO] Produto editado com sucesso!")
                self.close()
            else:
                QMessageBox.warning(self, "Erro", "Verifique sua conexão com a internet e o produto que está inserindo.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao inserir produto: {str(e)}")
