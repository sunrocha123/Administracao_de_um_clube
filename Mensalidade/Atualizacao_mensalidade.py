from datetime import date, datetime
from DB import conexaoDB
from Associado import Mecanismo

class Atualizacao(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    '''
    O caminho abaixo da acesso a engines de ajuste de data, coleta de endereço
    e validação de cadastro
    '''
    def conectar_engines(self):
        return Mecanismo.engines()

    def validar_cadastro(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao banco de dados...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...\n')
        else:
            ''' 
            Necessário validar se o nº do documento do usuário está cadastrado no DB.
            Caso esteja cadastrado, coletaremos o ID do cliente e a data de vencimento da mensalidade
            no banco de dados.
            '''

            print('Ponto de atenção: Para número de documento, digitar sem espaço e traço\n')

            print('========================')
            print('VALIDAÇÕES NECESSÁRIAS!')
            print('========================\n')

            n_documento = input('Digite o número do documento do associado: ').strip()
            dtVencimento = input('Digite a data de vencimento da mensalidade cadastrada: ').strip()

            #Validando se o usuário está cadastrado no banco de dados, com base no número do seu documento
            conn_DB.execute(f"SELECT ID_USUARIO FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            IDusuario = conn_DB.fetchval()

            #Validando se existe alguma mensalidade cadastrada no banco de dados, com base na data de vencimento informada
            conn_DB.execute(f"SELECT ID FROM MENSALIDADE WHERE DTVENCIMENTO = '{dtVencimento}' AND ID_USUARIO = {IDusuario}")
            IDmensalidade = conn_DB.fetchval()

            if IDusuario == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar...\n')
            elif IDusuario != None and IDmensalidade == None:
                print('Mensalidade não localizada no banco de dados...\n'
                    f'Por gentileza, verificar...\n')
            else:
                self.atualizar_mensalidade(conn_DB, IDusuario, IDmensalidade)

    def atualizar_mensalidade(self, conn_DB, IDusuario, IDmensalidade):

        print('\n====================================')
        print('CAMPOS DISPONÍVEIS PARA ATUALIZAÇÃO')
        print('====================================')
        print('\n1. Data de vencimento\n2. Data de pagamento\n3. Valor\n')

        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-3): '))
                if opcao == 1 or opcao == 2:
                    dataAtualizada = self.conectar_engines().ajustarData()
                    if opcao == 1:
                        conn_DB.execute(f"UPDATE MENSALIDADE SET DTVENCIMENTO = '{dataAtualizada}' WHERE ID = {IDmensalidade} AND ID_USUARIO = {IDusuario}")
                    else:
                        conn_DB.execute(f"UPDATE MENSALIDADE SET DTPAGAMENTO = '{dataAtualizada}' WHERE ID = {IDmensalidade} AND ID_USUARIO = {IDusuario}")
                    break
                elif opcao == 3:
                    valorAtualizado = float(input('Digite o valor atualizado: '))
                    conn_DB.execute(f"UPDATE MENSALIDADE SET VALOR = {valorAtualizado} WHERE ID = {IDmensalidade} AND ID_USUARIO = {IDusuario}")
                    break
                else:
                    print('Opção inválida! Digite novamente.....')
            except ValueError:
                print('Opção inválida! Digite novamente.....')

        conn_DB.commit()
        print(f'{datetime.now().strftime("%H:%M:%S")}: '
            f'Mensalidade atualizada!\n')
        pass