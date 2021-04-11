import pyodbc
from Acoes import DB
from datetime import date, datetime

class Associados(object):

    def conectar_DB(self):
        return DB.conectar()

    def cadastrar_novo_associado(self):
        print('\nDados pessoais\n')
        nome = input("Digite o nome (obrigatório): ").lower().strip()
        sobrenome = input("Digite o sobrenome (não obrigatório): ").lower().strip()
        tipo_documento = input("Digite o tipo de documento (obrigatório): ").lower().strip()
        numero_documento = input('Digite o número do documento (obrigatório): ').lower().strip()
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

        print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

        conn_DB = self.conectar_DB()

        if conn_DB == 0:
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')

        else:

            '''
            Neste trecho, validaremos se o nº do documento informado já consta no banco de dados.
            Caso já esteja, não será feita a inclusão do novo usuário. Caso contrário, daremos
            sequência na inclusão.
            '''            

            conn_DB.execute(f"SELECT NUMERO FROM DOCUMENTO WHERE NUMERO = '{numero_documento}'")
            validacao = conn_DB.fetchval()

            if validacao == None:

                try:
                    conn_DB.execute("INSERT INTO CLIENTE VALUES (?,?,?,GETDATE())",
                        nome, sobrenome, n_dependentes)

                    #Coletando o ID do usuário cadastrado
                    conn_DB.execute("SELECT MAX(ID) FROM CLIENTE")
                    IDcliente = conn_DB.fetchval()

                    #Trecho abaixo para cadastrado de documento no banco de dados

                    #Validando se o documento informado já consta no BD para coleta do ID
                    conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tipo_documento}'")
                    IDtipoDocumento = conn_DB.fetchval()

                    if IDtipoDocumento == None:
                        conn_DB.execute(f"INSERT INTO TIPO_DOCUMENTO (NOME) VALUES ('{tipo_documento}')")

                        #Coletando o ID do tipo do documento cadastrado
                        conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tipo_documento}'")
                        IDtipoDocumento = conn_DB.fetchval()
                    
                    conn_DB.execute("INSERT INTO DOCUMENTO VALUES (?,?,?,?,?)",
                                    IDcliente, IDtipoDocumento, numero_documento, dtEmissao, validacao)

                    self.cont_cadastrar_novo_associado(conn_DB, estado, cidade, tipo_endereco, IDcliente, tipo_logradouro, nome_logradouro, complemento, numero, bairro, cep)
                    conn_DB.commit()
                    print(f"{datetime.now().strftime('%H:%M:%S')}: Usuário cadastrado com sucesso!\n")
                except Exception as error:
                    print(f'\n{datetime.now().strftime("%H:%M:%S")}: {error}'
                        f'\nNão foi possível cadastrar o usuário. Estamos verificando o tema para solução do incidente!')
            else:
                print(f'O usuário de documento {tipo_documento}: {numero_documento} já está cadastrado\n'
                    f'Por gentileza, rever as informações coletadas...')     

        pass

    def cont_cadastrar_novo_associado(self, conn_DB, estado, cidade, tipoEndereco, IDCliente, tipoLogradouro, nomeLogradouro, complemento, numero, bairro, cep):
        #Trecho abaixo para cadastrado de endereço no banco de dados

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
        conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tipoEndereco}'") 
        IDtipoendereco = conn_DB.fetchval()

        if IDtipoendereco == None:
            conn_DB.execute(f"INSERT INTO TIPO_ENDERECO (NOME) VALUES ('{tipoEndereco}')")

            #Coletando o ID do tipo de endereço cadastrado
            conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tipoEndereco}'") 
            IDtipoendereco = conn_DB.fetchval()

        conn_DB.execute("INSERT INTO ENDERECO VALUES (?,?,?,?,?,?,?,?,?)",
                        IDCliente, IDtipoendereco, IDcidade,
                        tipoLogradouro, nomeLogradouro, complemento,
                        numero, bairro, cep)
        pass

    def alterar_associado(self):
        # Necessário validar se o nº do documento do usuário está cadastrado no DB
        print('Áreas de alteração\n1. Dados pessoais\n2. Endereço\n\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-2): '))
                if opcao == 1:
                    print('Campos Dados Pessoais\n')
                    camposDadosPessoais = ['nome', 'sobrenome', 'tipo_documento', 'numero_documento', 'dtEmissao', 'validade', 'n_dependentes']
                    for i in range(len(camposDadosPessoais)):
                        print((i + 1) + ". " + camposDadosPessoais[i])
                    break
                elif opcao == 2:
                    # Alteração de campos do endereço
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')         
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