"""
Módulo com a classe base para conexão com o banco de dados PostgreSQL.
"""

import psycopg2
from time import sleep
import os

class Bd_Base:
    """
    Classe base para conexão com o banco de dados PostgreSQL.
    """

    post_client = None

    def __init__(self) -> None:
        """
        Inicializa a conexão com o banco de dados.
        """
        if Bd_Base.post_client is None:
            self._conectar()

    def _conectar(self) -> None:
        """
        Conecta ao banco de dados PostgreSQL.
        """
        while True:
            try:
                host = os.getenv("POSTGRES_HOST", "localhost")
                Bd_Base.post_client = psycopg2.connect(
                    host=host,
                    database='database-postgres',
                    user='root',
                    password='root'
                )
                print("[LOG INFO] Conectado ao PostgreSQL em: ", host)
                break
            except psycopg2.OperationalError as e:
                print(f"[LOG ERRO] Erro ao conectar ao PostgreSQL: {e}")
                print("[LOG INFO] Tentando novamente em 2 segundos...")
                sleep(2)

    def get_cursor(self) -> psycopg2.extensions.cursor:
        """
        Retorna um cursor para a conexão com o banco de dados.

        Returns:
            psycopg2.extensions.cursor: Cursor para a conexão com o banco de dados.
        """
        if Bd_Base.post_client.closed:
            print("[LOG INFO] Conexão perdida. Tentando restabelecer...")
            self._reiniciar_coneccao()
        return Bd_Base.post_client.cursor()

    def _reiniciar_coneccao(self) -> None:
        """
        Reinicia a conexão com o banco de dados.
        """
        if Bd_Base.post_client is not None:
            try:
                Bd_Base.post_client.close()
                print("[LOG INFO] Conexão anterior fechada.")
            except Exception as e:
                print(f"[LOG ERRO] Erro ao fechar a conexão anterior: {e}")
        self._conectar()

    def commit(self) -> None:
        """
        Realiza o commit da transação.
        """
        qtd_tentativas = 0
        while True and qtd_tentativas < 3:
            try:
                Bd_Base.post_client.commit()
                break
            except Exception as e:
                print(f"[LOG ERRO] Erro ao tentar fazer commit: {e}")
                print("T[LOG INFO] Tentando reiniciar a conexão...")
                self._reiniciar_coneccao()
                qtd_tentativas += 1
        
        if qtd_tentativas == 3:
            print("[LOG ERRO] Não foi possível fazer commit após 3 tentativas. Encerrando...")
            exit(1)
