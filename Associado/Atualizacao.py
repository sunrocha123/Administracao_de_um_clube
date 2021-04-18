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
            ''' 
            Necessário validar se o nº do documento do usuário está cadastrado no DB.
            Caso esteja cadastrado, coletaremos o ID do cliente para realizar as atualizações necessárias.

            '''

            print('\nAntes de seguirmos com a atualização, precisamos realizar uma validação...')
            n_documento = input('Digite o número do documento do associado: ').lower().strip()

            conn_DB.execute(f"SELECT ID_CLIENTE FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            idCliente = conn_DB.fetchval()       

            if idCliente == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar!')
            
            else:
                self.coletar_dados(conn_DB, idCliente)
        pass

    def coletar_dados(self, conn_DB, idCliente):
        print('\nÁreas de alteração\n\n1. Dados pessoais\n2. Endereço\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-2): '))
                if opcao == 1:
                    self.escolherCampo_deAtualizacao_DadosPessoais(conn_DB, idCliente)
                    break
                elif opcao == 2:
                    self.escolherCampo_deAtualizacao_Endereco(conn_DB, idCliente)
                    break
                else:
                    print("Opção inválida! Digite novamente....")    
            except ValueError:
                print('Opção inválida! Digite novamente....')                
        pass

    def escolherCampo_deAtualizacao_DadosPessoais(self, conn_DB, idCliente):
        print('Campos Dados Pessoais\n')
        camposDadosPessoais = ['nome', 'sobrenome', 'n_dependentes', 'tipo_documento', 'numero', 'dtemissao', 'validade']
        for i in range(len(camposDadosPessoais)):
            print(str(i + 1) + ". " + camposDadosPessoais[i])
        print()
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-7): '))
                if opcao >= 1 and opcao <= 7:
                    if opcao >= 1 and opcao <= 3:
                        self.atualizarCliente(conn_DB, idCliente, camposDadosPessoais[opcao - 1])
                    else:
                        self.atualizarDocumento(conn_DB, idCliente, camposDadosPessoais[opcao - 1])
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')  
        pass

    def atualizarCliente(self, conn_DB, idCliente, campoAtualizacao):
        
        if campoAtualizacao == 'n_dependentes':
            novaIinformacao = int(input("Digite a nova informação: "))
        else:
            novaIinformacao = input("Digite a nova informação: ").lower().strip()

        try:
            conn_DB.execute(f"UPDATE CLIENTE SET {campoAtualizacao} = '{novaIinformacao}' WHERE ID = {idCliente}")
            conn_DB.commit()
            print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
                f'Informação atualizada com sucesso!')
        except Exception as error:
            print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                f'\nNão foi possível realizar a atualização. Estamos verificando o tema para solução do incidente!\n')

        pass

    def atualizarDocumento(self, conn_DB, idCliente, campoAtualizacao):
        if campoAtualizacao == 'tipo_documento':
            # Aguardando código
        else:
            if campoAtualizacao != 'numero':
                novaIinformacao = self.ajustarData()
            else:
                novaIinformacao = input("Digite nova informação: ").strip()

            try:
                conn_DB.execute(f"UPDATE DOCUMENTO SET {campoAtualizacao} = '{novaIinformacao}' WHERE ID = {idCliente}")
                conn_DB.commit()
                print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
                    f'Informação atualizada com sucesso!')
            except Exception as error:
                print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                    f'\nNão foi possível realizar a atualização. Estamos verificando o tema para solução do incidente!\n')
        pass

    def ajustarData(self):
        '''
        Está função tem como objetivo, arrumar a data informada pelo usuário
        no padrão YYYY-MM-DD para cadastro no banco de dados
        '''
        dataAjustada = ''

        dia = input('Digite o dia no formato DD: ')
        mes = input('Digite o mês no formato MM: ')
        ano = input('Digite o ano no formato YYYY: ')

        dataAjustada = ano + '-' + mes + '-' + dia

        return dataAjustada

    def escolherCampo_deAtualizacao_Endereco(self, conn_DB, idCliente):
        print('Campos Endereço\n')
        camposEndereco = ['tipo_endereco', 'tipo_logradouro', 'nome_logradouro', 'complemento', 'numero', 'bairro', 'cep', 'cidade', 'estado']
        for i in range(len(camposEndereco)):
            print(str(i + 1) + ". " + camposEndereco[i])
        print()
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-9): '))
                if opcao >= 1 and opcao <= 9:
                    if opcao >= 2 and opcao <= 7:
                        self.atualizarEndereco(conn_DB, idCliente, camposEndereco[opcao - 1])
                    elif opcao == 1:
                        # Aguardando código
                    else:
                        # Aguardando código
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')  
        pass

    def atualizarEndereco(self, conn_DB, idCliente, campoAtualizacao):
        novaInformacao = input("Digite a nova informação: ")

        try:
            conn_DB.execute(f"UPDATE ENDERECO SET {campoAtualizacao} = '{novaIinformacao}' WHERE ID = {idCliente}")
            conn_DB.commit()
            print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
                f'Informação atualizada com sucesso!')
        except Exception as error:
            print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                f'\nNão foi possível realizar a atualização. Estamos verificando o tema para solução do incidente!\n')

        pass