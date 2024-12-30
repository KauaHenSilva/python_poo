"""
Script: inicializa_cliente.py
Descrição: Este script inicializa um objeto da classe Cliente e o executa. Ao rodar o script, um objeto da classe
Cliente será instanciado e chamado para execução.

Classes:
    Cliente: Importada do módulo src.cliente. Representa um cliente em um sistema, e ao ser instanciada, realiza algum 
    tipo de operação ou processamento conforme a implementação da classe.

Execução:
    Ao executar este script diretamente (via terminal ou IDE), um objeto da classe Cliente será instanciado e chamado
    para realizar a ação associada ao seu funcionamento.
"""

# from src.cliente import Cliente

# if __name__ == "__main__":
#     Cliente()()

import sys
from sincronizacao_servidor_cliente.cliente_sincronizacao import ErroCliente
from src.screen.autenticacao import Autenticacao
from PyQt5.QtWidgets import QApplication, QMessageBox 
from src.screen.home_cliente_ui import Home

if __name__ == "__main__":
    app = QApplication(sys.argv)
    autenticacao = Autenticacao()
    autenticacao.show()
    app.exec_()
    
    if autenticacao.autenticado:
        try:
            window = Home()
            window.show()
            app.exec_()
        except ErroCliente as e:
            QMessageBox.critical(None, "ERROR", "Impossível conectar ao servidor.")
