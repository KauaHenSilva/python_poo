from .bd_postgree_base import Bd_Base
from typing import Union
import json
# criptografia
from passlib.hash import pbkdf2_sha256

class BdFuncionario(Bd_Base):

    def __init__(self) -> None:
        super().__init__()
        self.database_init()

    def database_init(self) -> None:
        try:
            cursor = self.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionario (
                    id SERIAL PRIMARY KEY,
                    usuario VARCHAR(255) UNIQUE,
                    senha VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL
                );
            """)

            self.commit()
        except Exception as e:
            print(f"[LOG ERRO] Não foi possível criar a tabela: {e}")
        finally:
            cursor.close()

    def _format_from_inserct(self, funcionario: str) -> dict:
        valor =  json.loads(funcionario)
        valor["senha"] = pbkdf2_sha256.hash(valor["senha"])
        return (valor['usuario'], valor["senha"], valor["email"])

    def insert_funcionario(self, funcionario: str) -> bool:
        retorno = True
        try:
            valor = self._format_from_inserct(funcionario)
            query = """
                INSERT INTO funcionario (usuario, senha, email)
                VALUES (%s, %s, %s)
            """
            cursor = self.get_cursor()
            cursor.execute(query, valor)
            self.commit()
            
        except Exception as e:
            print("[LOG ERRO] Erro ao inserir funcionario: ", e)
            self.post_client.rollback()
            retorno = False
        finally:
            cursor.close()

        return retorno

    def validar_acesso(self, usuario: str, senha: str) -> bool:
        retorno = False
        try:
            query = """
                SELECT * FROM funcionario 
                WHERE usuario = %s
            """
            cursor = self.get_cursor()
            cursor.execute(query, (usuario,))
            resultado = cursor.fetchone()
            
            if resultado:
                retorno = pbkdf2_sha256.verify(senha, resultado[2])  
               
            
        except Exception as e:
            print("[LOG ERRO] Erro ao validar acesso: ", e)
        finally:
            cursor.close()

        return retorno
