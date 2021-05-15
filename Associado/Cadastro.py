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
                    opcao_tipo_documento = int(input("Digite o tipo de documento (1-4) *: "))
                    if opcao_tipo_documento < 1 and opcao_tipo_documento > 4:
                        print('Opção inválida! Digite novamente...')
                    else:
                        if opcao_tipo_documento == 1:
                            tipo_documento = 'RG'
                        elif opcao_tipo_documento == 2:
                            tipo_documento = 'CPF'
                        elif opcao_tipo_documento == 3:
                            tipo_documento == 'Carteira de trabalho'
                        else:
                            tipo_documento = 'Titulo de eleitor'
                        break
                except ValueError:
                    print('Opção inválida! Digite novamente...')

            numero_documento = input('Digite o número do documento *: ').strip()
            dtEmissao = input('Digite a data de emissão do documento: ').strip()
            validade = input('Digite a data de validade do documento: ').strip()

            print('\nTipo de telefone:\n1. Particular\n2. Corporativo\n')

            while True:
                try:
                    opcao_tipo_telefone = int(input("Digite o tipo de telefone (1-2) *: "))
                    if opcao_tipo_telefone != 1 and opcao_tipo_telefone != 2:
                        print('Opção inválida! Digite novamente...')
                    else:
                        if opcao_tipo_telefone == 1:
                            tipo_telefone = 'Particular'
                        else:
                            tipo_telefone = 'Corporativo'
                        break
                except ValueError:
                    print('Opção inválida! Digite novamente...')

            DDDtelefone = input('Digite o DDD *: ')
            n_telefone = input('Digite o número *: ')          
            
            try:
                n_dependentes = int(input("Digite o número de dependentes: "))
            except ValueError:
                n_dependentes = 0

            '''Tendo o CEP, será coletado o endereço completo via API'''
            endereco = self.coletar_endereco()
            if endereco == 0:
                print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
                f'Por gentileza, tente mais tarde...')
            else:
                print(f'\nEndereço localizado:\n'
                        f'Logradouro: {endereco["address"]}\n'
                        f'Cidade: {endereco["city"]}\n'
                        f'Estado: {endereco["state"]}\n'
                        f'Bairro: {endereco["district"]}\n'
                        f'CEP: {endereco["code"]}\n')
                numero = input('Digite o número: ').strip()
                complemento = input("Digite o complemento: ").lower().strip()
                print('\nTipo endereço:\n1. Residencial\n2. Corporativo\n')

                while True:
                    try:
                        opcao_tipo_endereco = int(input("Digite o tipo de endereço (1-2) *: "))
                        if opcao_tipo_endereco != 1 and opcao_tipo_endereco != 2:
                            print('Opção inválida! Digite novamente...')
                        else:
                            if opcao_tipo_endereco == 1:
                                tipo_endereco = 'Residencial'
                            else:
                                tipo_endereco = 'Corporativo'
                            break
                    except ValueError:
                        print('Opção inválida! Digite novamente...')
            
                if self.validar_cadastro(conn_DB, numero_documento) == 0:
                    print(f'O usuário de documento {tipo_documento}: {numero_documento} já está cadastrado\n'
                        f'Por gentileza, rever as informações coletadas...\n')
                else:
                    try:
                        usuario = self.cadastrar_usuario(nome, sobrenome, n_dependentes, conn_DB) # cadastra o usuário e coleta o ID gerado para o mesmo
                        telefone = self.cadastrar_telefone(tipo_telefone, usuario, DDDtelefone, n_telefone, conn_DB)
                        documento = self.cadastrar_documento(conn_DB, usuario, numero_documento, dtEmissao, validade, tipo_documento)
                        endereco = self.cadastrar_endereco(conn_DB, usuario, tipo_endereco, endereco, complemento, numero)
                        conn_DB.commit()
                        print()
                        print(f"{datetime.now().strftime('%H:%M:%S')}: Usuário cadastrado com sucesso!\n")
                    except Exception as error:
                        print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                                f'\nNão foi possível cadastrar o usuário. Estamos verificando o tema para solução do incidente!\n')  

    def coletar_endereco(self):
        try:           
            cep = input('Digite o CEP *: ').strip()
            print(f"\n{datetime.now().strftime('%H:%M:%S')}: "
                f"Conectando a API....") 
            response = requests.get(f'https://ws.apicep.com/cep/{cep}.json')
            print(f"{datetime.now().strftime('%H:%M:%S')}: "
                f"Conexão realizada com sucesso!")
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return 0

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

    def cadastrar_usuario(self, nome, sobrenome, n_dependentes, conn_DB):

        #Cadastrando usuário no banco de dados
        conn_DB.execute("INSERT INTO USUARIO VALUES (?,?,?,GETDATE())",
                        nome, sobrenome, n_dependentes)

        #Coletando o ID do usuário cadastrado
        conn_DB.execute("SELECT MAX(ID) FROM USUARIO")
        IDusuario = conn_DB.fetchval()

        return IDusuario

    def cadastrar_telefone(self, tipo_telefone, IDusuario, DDD, n_telefone, conn_DB):
        #Coletando o ID do tipo de telefone
        conn_DB.execute(f"SELECT ID FROM TIPO_TELEFONE WHERE NOME = '{tipo_telefone}'")
        Idtipo_telefone = conn_DB.fetchval()

        #Cadastrando telefone no banco de dados
        conn_DB.execute("INSERT INTO VALUES (?,?,?,?)",
                        IDusuario, Idtipo_telefone, DDD, n_telefone)
        pass          

    def cadastrar_documento(self, conn_DB, IDusuario, numero_documento, dtEmissao, validade, tipo_documento):

        #Coletando o ID do tipo do documento
        conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tipo_documento}'")
        IDtipo_documento = conn_DB.fetchval()

        #Cadastrando documento no banco de dados            
        conn_DB.execute("INSERT INTO DOCUMENTO VALUES (?,?,?,?,?)",
                        IDusuario, IDtipo_documento, numero_documento, dtEmissao, validade)

    def cadastrar_endereco(self, conn_DB, IDusuario, tipo_endereco, endereco, complemento, numero):
        #Coletando o ID do tipo de endereço
        conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tipo_endereco}'")
        IDtipo_endereco = conn_DB.fetchval()

        #Validando se o CEP informado já encontrasse no banco de dados
        conn_DB.execute(f"SELECT ID FROM CEP WHERE NUMERO = '{endereco['code']}'")
        IDcep = conn_DB.fetchval()

        if IDcep == None:
            #Aguardando código de cadastro de endereço no banco
            pass

        conn_DB.execute("INSERT INTO ENDERECO VALUES (?,?,?,?,?)",
                        IDusuario, IDtipo_endereco, IDcep,
                        numero, complemento)
