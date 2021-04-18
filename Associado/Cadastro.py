import pyodbc
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
            print('\nDados pessoais\n')
            nome = input("Digite o nome (obrigatório): ").lower().strip()
            sobrenome = input("Digite o sobrenome (não obrigatório): ").lower().strip()
            tipo_documento = input("Digite o tipo de documento (obrigatório): ").lower().strip()
            numero_documento = input('Digite o número do documento (obrigatório): ').strip()
            dtEmissao = input('Digite a data de emissão do documento **Formato: aaaa - mm - dd** (não obrigatório): ').strip()
            validade = input('Digite a data de validade do documento **Formato: aaaa - mm - dd** (não obrigatório): ').strip()
            
            try:
                n_dependentes = int(input("Digite o número de dependentes (não obrigatório): "))
            except ValueError:
                n_dependentes = 0


            print('\nEndereço\n')
            tipo_endereco = input("Digite o tipo de endereço (obrigatório): ").lower().strip()
            tipo_logradouro = input("Digite o tipo de logradouro (obrigatório): ").lower().strip()
            nome_logradouro = input("Digite o nome do logradouro (obrigatório): ").lower().strip()
            complemento = input("Digite o complemento (não obrigatório): ").lower().strip()
            numero = input('Digite o número (não obrigatório): ').strip()
            bairro = input('Digite o bairro (obrigatório): ').lower().strip()
            cep = input('Digite o CEP (não obrigatório): ').strip()
            cidade = input('Digite a cidade (obrigatório): ').lower().strip()
            estado = input('Digite o estado (obrigatório): ').lower().strip()

            if self.validar_cadastro(conn_DB, numero_documento) == 0:
                print(f'O usuário de documento {tipo_documento}: {numero_documento} já está cadastrado\n'
                    f'Por gentileza, rever as informações coletadas...\n')
            else:
                try:
                    cliente = self.cadastrar_cliente(nome, sobrenome, n_dependentes, conn_DB) # cadastra o usuário e coleta o ID gerado para o mesmo
                    documento = self.cadastrar_documento(conn_DB, cliente, numero_documento, dtEmissao, validade, tipo_documento)
                    endereco = self.cadastrar_endereco(conn_DB, cliente, tipo_endereco, tipo_logradouro, nome_logradouro, complemento, numero, bairro, cep, cidade, estado)
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

    def cadastrar_endereco(self, conn_DB, IDcliente, tipo_endereco, tipo_logradouro, nome_logradouro, complemento, numero, bairro, cep, cidade, estado):
        '''Trecho para cadastrado de endereço no banco de dados'''

        #Validando se o estado informado já consta no BD para coleta do ID
        conn_DB.execute(f"SELECT ID FROM ESTADO WHERE NOME = '{estado}'")
        IDestado = conn_DB.fetchval()

        if IDestado == None:
            conn_DB.execute(f"INSERT INTO ESTADO (NOME) VALUES ('{estado}')")

            #Coletando o ID do estado cadastrado
            conn_DB.execute(f"SELECT ID FROM ESTADO WHERE NOME = '{estado}'")
            IDestado = conn_DB.fetchval()

        #Validando se a cidade informado já consta no BD para coleta do ID
        conn_DB.execute(f"SELECT ID FROM CIDADE WHERE NOME = '{cidade}'")
        IDcidade = conn_DB.fetchval()

        if IDcidade == None:
            conn_DB.execute(f"INSERT INTO CIDADE VALUES (?, ?)", IDestado, cidade)

            #Coletando o ID da cidade cadastrado
            conn_DB.execute(f"SELECT ID FROM CIDADE WHERE NOME = '{cidade}'")
            IDcidade = conn_DB.fetchval()

        #Validando se o tipo de endereço informado já consta no BD para coleta do ID
        conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tipo_endereco}'") 
        IDtipoendereco = conn_DB.fetchval()

        if IDtipoendereco == None:
            conn_DB.execute(f"INSERT INTO TIPO_ENDERECO (NOME) VALUES ('{tipo_endereco}')")

            #Coletando o ID do tipo de endereço cadastrado
            conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tipo_endereco}'") 
            IDtipoendereco = conn_DB.fetchval()

        conn_DB.execute("INSERT INTO ENDERECO VALUES (?,?,?,?,?,?,?,?,?)",
                        IDcliente, IDtipoendereco, IDcidade,
                        tipo_logradouro, nome_logradouro, complemento,
                        numero, bairro, cep)
