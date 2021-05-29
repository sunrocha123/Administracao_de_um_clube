import pyodbc
from datetime import date, datetime
from DB import conexaoDB

class Cadastro(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    def coletar_dados(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao banco de dados...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')
        else:
            print(f'Pontos de atenção:\n'
                    f'1. Todo campo que tiver um * no final, é obrigatório o preenchimento!\n'
                    f'2. Para número de documento, digitar sem espaço e traço\n'
                    f'3. Para campos que solicitam data, digitar no formato AAAA-MM-DD\n')

            '''
            As mensalidades cadastradas no banco de dados, serão associadas ao número do documento
            do usuário
            '''

            print('Antes de seguirmos com o cadastro, precisamos realizar uma validação...\n')

            nDocumento = input('Digite o número do documento do associado: ').strip()

            #Validando se o usuário existe no banco de dados, com base no seu número de documento
            conn_DB.execute(f"SELECT ID FROM DOCUMENTO WHERE NUMERO = '{nDocumento}'")
            idUsuario = conn_DB.fetchval()

            if idUsuario == None:
                print(f'Usuário não localizado no banco de dados, desta forma, não é possível seguir com o cadastrado da mensalidade\n'
                    f'Por gentileza, verificar...\n')

            else:
                dtVencimento = input('Digite a data de vencimento *: ').strip()
                valor = float(input('Digite o valor *: '))
                dtPagamento = input('Digite a data de pagamento: ').strip()

                if dtPagamento == '':
                    dtPagamento = None

                self.cadastrar_mensalidade(conn_DB, dtVencimento, valor, dtPagamento, idUsuario)
                print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
                f'Mensalidade cadastrada!')

    def cadastrar_mensalidade(self, conn_DB, dtVencimento, valor, dtPagamento, idUsuario):

        #Cadastrando mensalidade
        conn_DB.execute("INSERT INTO MENSALIDADE VALUES (?,?,?,?)",
                        idUsuario, dtVencimento, valor, dtPagamento)
        conn_DB.commit()
        pass