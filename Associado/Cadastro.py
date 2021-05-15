import pyodbc
import requests
from datetime import date, datetime
from DB import conexaoDB

class Cadastro(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

    def coletar_dados(self):
        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')
        else:
            print(f'Por gentileza, informe os dados abaixo para cadastro do usuário\n\nPontos de atenção:\n'
                    f'1. Todo campo que tiver um * no final, é obrigatório o preenchimento!\n'
                    f'2. Para número de documento, digitar sem espaço e traço\n'
                    f'3. Para campos que solicitam data, digitar no formato AAAA-MM-DD\n'
                    f'4. Para o campo de CEP, digitar no formato 00000-000\n')

            nome = input("Digite o nome *: ").lower().strip()
            sobrenome = input("Digite o sobrenome: ").lower().strip()

            print('\nTipo de documento:\n1. RG\n2. CPF\n3. Carteira de trabalho\n4. Título de eleitor\n5. CNH\n')
            while True:
                try:
                    tipo_documento = int(input("Digite o tipo de documento (1-4) *: "))
                    if tipo_documento < 1 and tipo_documento > 4:
                        print('Opção inválida! Digite novamente...')
                    else:
                        break
                except ValueError:
                    print('Opção inválida! Digite novamente...')

            numero_documento = input('Digite o número do documento *: ').strip()
            dtEmissao = input('Digite a data de emissão do documento: ').strip()
            validade = input('Digite a data de validade do documento: ').strip()
            
            try:
                n_dependentes = int(input("Digite o número de dependentes: "))
            except ValueError:
                n_dependentes = 0

            '''Tendo o CEP, será coletado o endereço completo via API'''
            cep = input('Digite o CEP *: ').strip()
            response = requests.get(f'https://ws.apicep.com/cep/{cep}.json')
            dados = response.json()
            print(dados)
            complemento = input("Digite o complemento: ").lower().strip()
            numero = input('Digite o número: ').strip()
            

            if self.validar_cadastro(conn_DB, numero_documento) == 0:
                print(f'O usuário de documento {tipo_documento}: {numero_documento} já está cadastrado\n'
                    f'Por gentileza, rever as informações coletadas...\n')
            else:
                try:
                    cliente = self.cadastrar_cliente(nome, sobrenome, n_dependentes, conn_DB) # cadastra o usuário e coleta o ID gerado para o mesmo
                    documento = self.cadastrar_documento(conn_DB, cliente, numero_documento, dtEmissao, validade, tipo_documento)
                    endereco = self.cadastrar_endereco(conn_DB, cliente, complemento, numero)
                    conn_DB.commit()
                    print()
                    print(f"{datetime.now().strftime('%H:%M:%S')}: Usuário cadastrado com sucesso!\n")
                except Exception as error:
                    print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                            f'\nNão foi possível cadastrar o usuário. Estamos verificando o tema para solução do incidente!\n')  


    def validar_cadastro(self, conn_DB, numero_documento):

        '''
        Neste trecho, validaremos se o nº do documento informado já consta no banco de dados.
        Caso já esteja, não será feita a inclusão do novo usuário. Caso contrário, daremos
        sequência na inclusão.
        '''  
        conn_DB.execute(f"SELECT NUMERO FROM DOCUMENTO WHERE NUMERO = '{numero_documento}'")
        validacao = conn_DB.fetchval()
        if validacao == None:
            return 1
        else:
            return 0            
        pass

    def cadastrar_cliente(self, nome, sobrenome, n_dependentes, conn_DB):
        conn_DB.execute("INSERT INTO CLIENTE VALUES (?,?,?,GETDATE())",
                        nome, sobrenome, n_dependentes)

        #Coletando o ID do usuário cadastrado
        conn_DB.execute("SELECT MAX(ID) FROM CLIENTE")
        IDcliente = conn_DB.fetchval()

        return IDcliente           

    def cadastrar_documento(self, conn_DB, IDcliente, numero_documento, dtEmissao, validade, tipo_documento):
        '''Trecho para cadastrado de documento no banco de dados'''

        #Validando se o documento informado já consta no BD para coleta do ID
        conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tipo_documento}'")
        IDtipoDocumento = conn_DB.fetchval()

        if IDtipoDocumento == None:
            conn_DB.execute(f"INSERT INTO TIPO_DOCUMENTO (NOME) VALUES ('{tipo_documento}')")

            #Coletando o ID do tipo do documento cadastrado
            conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tipo_documento}'")
            IDtipoDocumento = conn_DB.fetchval()
                        
        conn_DB.execute("INSERT INTO DOCUMENTO VALUES (?,?,?,?,?)",
                        IDcliente, IDtipoDocumento, numero_documento, dtEmissao, validade)

    def cadastrar_endereco(self, conn_DB, IDcliente, complemento, numero, cep):
        '''Trecho para cadastrado de endereço no banco de dados'''

        conn_DB.execute("INSERT INTO ENDERECO VALUES (?,?,?,?,?,?,?,?,?)",
                        IDcliente, IDtipoendereco, IDcidade,
                        tipo_logradouro, nome_logradouro, complemento,
                        numero, bairro, cep)
