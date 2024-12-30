import json
from funcao_postgree.bd_postgree_funcionario import BdFuncionario

bd_funcionario = BdFuncionario()

def inserir_funcionario(funcionario: dict[str, str]) -> bool:
    bd_funcionario.insert_funcionario(json.dumps(funcionario))

def validar_acesso(usuario: str, senha: str) -> bool:
    return bd_funcionario.validar_acesso(usuario, senha)