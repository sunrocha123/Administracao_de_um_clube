import pyodbc
from Acoes import DB
from datetime import date, datetime

class Associados(object):

    def conectar_DB(self):
        return DB.conectar()

    def cadastrar_novo_associado(self):
        nome = input("Digite o nome: ").title().strip()
        sobrenome = input("Digite o sobrenome: ").title().strip()
        cpf = input("Digite o CPF **Sem traço e ponto**: ").strip()
        n_dependentes = int(input("Digite o número de dependentes: "))

        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')

        else:
            try:
                conn_DB.execute("INSERT INTO USUARIO VALUES (?,?,?,?,GETDATE())",
                    cpf, nome, sobrenome, n_dependentes)
                conn_DB.commit()
                print("Usuário cadastrado com sucesso!\n")
            except Exception as error:
                print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                    f'\nNão foi possível cadastrar o usuário. Estamos verificando o tema para solução do incidente!')              

        pass

    def alterar_associado(self):
        # Pendente criação
        pass

    def excluir_associado(self):
        cpf = input("Digite o CPF do associado **Sem traço e ponto**: ").strip()
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()
        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')
        else:
            try:
                conn_DB.execute(f"DELETE FROM USUARIO WHERE CPF = {cpf}")
                conn_DB.commit()
                print('Usuário deletado com sucesso!\n')
            except Exception as error:
                print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                    f'\nNão foi possível deletar o usuário. Estamos verificando o tema para solução do incidente!')  
        pass