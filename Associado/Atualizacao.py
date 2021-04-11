import pyodbc
from datetime import date, datetime
from DB import conexaoDB

class Atualizacao(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    def validar_cadastro(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')
        else:
            # Necessário validar se o nº do documento do usuário está cadastrado no DB
            print('\nAntes de seguirmos com a atualização, precisamos realizar uma validação...')
            n_documento = input('Digite o número do documento do associado: ').lower().strip()

            conn_DB.execute(f"SELECT NUMERO FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            validacao = conn_DB.fetchval()       

            if validacao == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar!')
            
            else:
                self.coletar_dados(conn_DB)
        pass

    def coletar_dados(self, conn_DB):
        print('\nÁreas de alteração\n\n1. Dados pessoais\n2. Endereço\n\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-2): '))
                if opcao == 1:
                    self.atualizar_DadosPessoais(conn_DB)
                    break
                elif opcao == 2:
                    self.atualizar_Endereco(conn_DB)
                    break
                else:
                    print("Opção inválida! Digite novamente....")    
            except ValueError:
                print('Opção inválida! Digite novamente....')                
        pass

    def atualizar_DadosPessoais(self, conn_DB):
        print('Campos Dados Pessoais\n')
        camposDadosPessoais = ['nome', 'sobrenome', 'tipo_documento', 'numero_documento', 'dtEmissao', 'validade', 'n_dependentes']
        for i in range(len(camposDadosPessoais)):
            print(str(i + 1) + ". " + camposDadosPessoais[i])
        print()
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-7): '))
                if opcao >= 1 and opcao <= 7:
                    #Aguardando código
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')  
        pass

    def atualizar_Endereco(self, conn_DB):
        print('Campos Endereço\n')
        camposEndereco = ['tipo_endereco', 'tipo_logradouro', 'nome_logradouro', 'complemento', 'numero', 'bairro', 'cep', 'cidade', 'estado']
        for i in range(len(camposEndereco)):
            print(str(i + 1) + ". " + camposEndereco[i])
        print()
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-9): '))
                if opcao >= 1 and opcao <= 9:
                    #Aguardando código
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')  
        pass