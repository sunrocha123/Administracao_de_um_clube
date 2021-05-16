import pyodbc
from datetime import date, datetime
from DB import conexaoDB

class Atualizacao(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    def validar_cadastro(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao banco de dados...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')
        else:
            ''' 
            Necessário validar se o nº do documento do usuário está cadastrado no DB.
            Caso esteja cadastrado, coletaremos o ID do cliente para realizar as atualizações necessárias.

            '''

            print(f'\nAntes de seguirmos com a atualização, precisamos realizar uma validação...\n'
                f'Digite o campo abaixo sem ponto e traço\n')
            n_documento = input('Digite o número do documento do associado: ').lower().strip()

            conn_DB.execute(f"SELECT ID_USUARIO FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            IDusuario = conn_DB.fetchval()       

            if IDusuario == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar...')
            
            else:
                self.escolher_setor_de_atualizacao(conn_DB, IDusuario)
        pass

    def escolher_setor_de_atualizacao(self, conn_DB, IDusuario):
        print('\nÁreas de alteração\n\n1. Usuário\n2. Documento\n3. Telefone\n4. Endereço\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-4): '))
                if opcao == 1:
                    self.atualizar_usuario(conn_DB, IDusuario)
                    break
                elif opcao == 2:
                    self.atualizar_documento(conn_DB, IDusuario)
                    break
                elif opcao == 3:
                    self.atualizar_telefone(conn_DB, IDusuario)
                    break
                elif opcao == 4:
                    self.atualizar_endereco(conn_DB, IDusuario)
                    break
                else:
                    print("Opção inválida! Digite novamente....")    
            except ValueError:
                print('Opção inválida! Digite novamente....')                
        pass

    def atualizar_usuario(self, conn_DB, IDusuario):
        print('\n1. Nome\n2. Sobrenome\n3. Número de dependentes\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-3): '))
                if opcao == 3:
                    while True:
                        try:
                            novaInformacao = int(input('Digite a nova informação: '))
                            break
                        except ValueError:
                            print('Opção inválida! Digite novamente.....')
                    conn_DB.execute(f"UPDATE USUARIO SET N_DEPENDENTES = {novaInformacao}")
                else:
                    novaInformacao = input('Digite a nova informação: ').lower().strip()
                    if opcao == 1:
                        coluna = 'NOME'
                    elif opcao == 2:
                        coluna = 'SOBRENOME'
                    conn_DB.execute(f"UPDATE USUARIO SET {coluna} = '{novaInformacao}'")
                conn_DB.commit()
                print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")
                break
            except ValueError:
                print('Opção inválida! Digite novamente.....')
    def atualizar_documento(self, conn_DB, idCliente, campoAtualizacao):
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

    def atualizar_endereco(self, conn_DB, idCliente): 
        pass

    def atualizar_telefone(self, conn_DB, IDusuario):
        pass