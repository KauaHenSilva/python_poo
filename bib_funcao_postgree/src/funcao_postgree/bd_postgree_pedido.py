"""
Modulo responsável por realizar a comunicação com o banco de dados dos pedidos.
"""

from .bd_postgree_base import Bd_Base
from typing import Union
import json


class BdPedido(Bd_Base):
    """
    Classe para manipulação de dados da tabela Pedido no banco de dados PostgreSQL.

    Essa classe gerencia a estrutura da tabela Pedido e permite realizar operações
    como inserção, atualização e consulta de pedidos.
    """

    def __init__(self, host: str = 'localhost', database: str = 'database-postgres', user: str = 'root', password: str = 'root') -> None:
        """
        Inicializa a conexão com o banco de dados e cria a tabela Pedido caso ela não exista.

        Args:
            host (str): Endereço do host do banco de dados.
            database (str): Nome do banco de dados.
            user (str): Nome de usuário para autenticação.
            password (str): Senha para autenticação.
        """
        super().__init__(host, database, user, password)
        self.database_init()

    def database_init(self) -> None:
        """
        Cria a tabela Pedido no banco de dados caso ela não exista.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pedido (
                    id SERIAL PRIMARY KEY,
                    mesa INT NOT NULL,
                    status VARCHAR(255) NOT NULL,
                    data_hora TIMESTAMP NOT NULL
                );
            """)
            self.commit()
            print("[LOG INFO] Tabela inicializada com sucesso!")
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()

    def editar_status(self, status: str, id_pedido: int) -> bool:
        """
        Edita o status de um pedido no banco de dados.

        Args:
            status (str): Novo status do pedido.
            id_pedido (int): ID do pedido a ser editado.

        Returns:
            bool: True se a edição foi bem-sucedida, False caso contrário.
        """
        retorno = True
        try:
            query = """
                UPDATE Pedido 
                SET status = %s
                WHERE id = %s
            """
            cursor = self.get_cursor()
            cursor.execute(query, (status, id_pedido))
            self.commit()
        except Exception as e:
            print("[LOG ERRO] Erro ao editar status do pedido: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def _format_from_inserct(self, pedido: str) -> dict:
        """
        Formata os dados do pedido para inserção no banco de dados.

        Args:
            pedido (str): Dados do pedido em formato JSON.

        Returns:
            dict: Dicionário contendo os dados formatados para inserção.
        """
        valor = json.loads(pedido)
        return (valor['mesa'], valor["status"], valor["data_hora"])

    def insert_pedido(self, pedido: str) -> bool:
        """
        Insere um pedido no banco de dados.

        Args:
            pedido (str): Dados do pedido em formato JSON.

        Returns:
            bool: True se a inserção foi bem-sucedida, False caso contrário.
        """
        retorno = True
        try:
            valor = self._format_from_inserct(pedido)
            query = """
                INSERT INTO Pedido (mesa, status, data_hora) 
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
        except Exception as e:
            print("[LOG ERRO] Erro ao inserir pedido: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def get_last_1000(self) -> Union[list, None]:
        """
        Retorna os 1000 últimos pedidos do banco de dados.

        Returns:
            Union[list, None]: Lista com os pedidos ou None em caso de erro.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido ORDER BY id DESC LIMIT 1000;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()

    def get_all(self) -> Union[list, None]:
        """
        Retorna todos os pedidos do banco de dados.

        Returns:
            Union[list, None]: Lista com os pedidos ou None em caso de erro.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM Pedido;")
            resultados = cursor.fetchall()
            return resultados
        except Exception:
            return None
        finally:
            cursor.close()

    def get_pedidos_csv(self) -> str:
        """
        Busca os pedidos do banco de dados e converte para um texto CSV.

        Returns:
            str: Texto CSV com os pedidos ou uma string vazia em caso de erro.
        """
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                SELECT * FROM Pedido;
            """)

            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]

            csv_text = ",".join(headers) + "\n"
            for row in rows:
                csv_text += ",".join(str(cell) for cell in row) + "\n"
            return csv_text
        except Exception as e:
            print(f"[LOG ERRO] Erro ao buscar pedidos: {e}")
            return ""
        finally:
            cursor.close()
