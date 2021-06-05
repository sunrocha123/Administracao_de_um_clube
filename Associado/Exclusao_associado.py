import pyodbc
from datetime import date, datetime
from DB import conexaoDB

class Exclusao(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    def validar_cadastro(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao banco de dados...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...\n')
        else:
            '''
            Para excluir os dados do usuário do banco de dados, usaremos o número do seu documento
            cadastrado.
            '''
            print(f'Pontos de atenção: Para número de documento, digitar sem espaço e traço\n')

            nDocumento = input("Digite o número do documento do associado: ").strip()

            #Validando se o usuário está cadastrado no banco de dados, com base no número do documento
            conn_DB.execute(f"SELECT ID_USUARIO FROM DOCUMENTO WHERE NUMERO = '{nDocumento}'")
            IDassociado = conn_DB.fetchval()

            if IDassociado == None:
                print(f'Usuário não localizado no banco de dados...\n'
                f'Por gentileza, verificar...\n')
            else:
                self.excluir_dados(conn_DB, IDassociado)

    def excluir_dados(self, conn_DB, IDassociado):

        #Deletando o telefone do usuário do banco de dados
        conn_DB.execute(f"DELETE FROM TELEFONE WHERE ID_USUARIO = {IDassociado}")

        #Deletando mensalidade do usuário do banco de dados
        conn_DB.execute(f"DELETE FROM MENSALIDADE WHERE ID_USUARIO = {IDassociado}")

        #Deletando o documento do usuário do banco de dados
        conn_DB.execute(f"DELETE FROM DOCUMENTO WHERE ID_USUARIO = {IDassociado}")

        #Deletando o endereço do usuário do banco de dados
        conn_DB.execute(f"DELETE FROM ENDERECO WHERE ID_USUARIO = {IDassociado}")

        #Deletando o usuário do banco de dados
        conn_DB.execute(f"DELETE FROM USUARIO WHERE ID = {IDassociado}")

        conn_DB.commit()

        print(f'{datetime.now().strftime("%H:%M:%S")}: '
            f'Dados excluídos!\n')