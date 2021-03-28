import pyodbc
from Acoes import DB
from datetime import date, datetime

class Associados(object):

    def conectar_DB(self):
        return DB.conectar()

    def cadastrar_novo_associado(self):
        print('\nDados pessoais\n')
        nome = input("Digite o nome (obrigatório): ").title().strip()
        sobrenome = input("Digite o sobrenome (não obrigatório): ").title().strip()
        tipo_documento = input("Digite o tipo de documento (obrigatório): ").strip().title()
        numero_documento = input('Digite o número do documento (obrigatório): ').strip()
        dtEmissao = input('Digite a data de emissão do documento **Formato: aaaa - mm - dd** (não obrigatório): ').strip()
        validade = input('Digite a data de validade do documento **Formato: aaaa - mm - dd** (não obrigatório): ').strip()
        n_dependentes = int(input("Digite o número de dependentes (não obrigatório): "))

        '''print('\nEndereço\n')
        tipo_endereco = input("Digite o tipo de endereço (obrigatório): ").title().strip()
        tipo_logradouro = input("Digite o tipo de logradouro (obrigatório): ").title().strip()
        nome_logradouro = input("Digite o nome do logradouro (obrigatório): ").title().strip()
        complemento = input("Digite o complemento (não obrigatório): ").title().strip()
        numero = input('Digite o número (não obrigatório): ').strip()
        bairro = input('Digite o bairro (obrigatório): ').strip()
        cep = input('Digite o CEP (não obrigatório): ').strip()
        cidade = input('Digite a cidade (obrigatório): ').title().strip()
        estado = input('Digite o estado (obrigatório): ').title().strip()'''

        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')

        else:
            try:
                conn_DB.execute("INSERT INTO CLIENTE VALUES (?,?,?,GETDATE())",
                    nome, sobrenome, n_dependentes)
                conn_DB.commit()
                print(f"{datetime.now().strftime("%H:%M:%S")}: Usuário cadastrado com sucesso!\n")
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