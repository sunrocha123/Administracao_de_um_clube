import pyodbc
from datetime import date, datetime
from DB import conexaoDB
from Associado import Cadastro

class Atualizacao(object):

    def conectar_DB(self):
        return conexaoDB.conectar()

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
            Caso esteja cadastrado, coletaremos o ID do cliente para realizar as atualizações necessárias.

            '''
            print(f'\nPontos de atenção:\n'
                    f'1. Para número de documento, digitar sem espaço e traço\n'
                    f'2. Para o campo de CEP, digitar no formato 00000-000\n')
        
            print('\nAntes de seguirmos com a atualização, precisamos realizar uma validação...\n')

            n_documento = input('Digite o número do documento do associado: ').lower().strip()

            conn_DB.execute(f"SELECT ID_USUARIO FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            IDusuario = conn_DB.fetchval()       

            if IDusuario == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar...\n')
            
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
                    conn_DB.execute(f"UPDATE USUARIO SET N_DEPENDENTES = {novaInformacao} WHERE ID = {IDusuario}")
                else:
                    novaInformacao = input('Digite a nova informação: ').lower().strip()
                    if opcao == 1:
                        coluna = 'NOME'
                    elif opcao == 2:
                        coluna = 'SOBRENOME'
                    conn_DB.execute(f"UPDATE USUARIO SET {coluna} = '{novaInformacao}' WHERE ID = {IDusuario}")
                conn_DB.commit()
                print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")
                break
            except ValueError:
                print('Opção inválida! Digite novamente.....')

    def atualizar_documento(self, conn_DB, IDusuario):
        print('\n1. Tipo de documento\n2. Numero\n3. Data de emissão\n4. Validade\n')

        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-4): '))
                if opcao == 1:
                    print('\nTipos de documentos disponíveis\n')
                    tdocumentos = ['RG', 'CPF', 'Carteira de trabalho', 'Titulo de eleitor', 'CNH']

                    for i in range(len(tdocumentos)):
                        print(str(i + 1) + ". " + tdocumentos[i])
                    print()
                    while True:
                        try:
                            novaInformacao = int(input('Digite a nova informação (1-5): '))
                            break
                        except ValueError:
                            print('Opção inválida! Digite novamente.....')

                    #Coletar ID do tipo de documento no banco de dados
                    conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tdocumentos[novaInformacao - 1]}'")
                    idTipoDocumento = conn_DB.fetchval()

                    #Atualizando tipo de documento do usuário
                    conn_DB.execute(f"UPDATE DOCUMENTO SET ID_TIPO_DOCUMENTO = {idTipoDocumento} WHERE ID_USUARIO = {IDusuario}")
                elif opcao == 3 or opcao == 4:
                    dataAtualizada = self.ajustarData()
                    if opcao == 3:
                        conn_DB.execute(f"UPDATE DOCUMENTO SET DTEMISSAO = '{dataAtualizada}' WHERE ID_USUARIO = {IDusuario}")
                    else:
                        conn_DB.execute(f"UPDATE DOCUMENTO SET VALIDADE = '{dataAtualizada}' WHERE ID_USUARIO = {IDusuario}")
                else:
                    novaInformacao = input('Digite a nova informação: ').strip()
                    conn_DB.execute(f"UPDATE DOCUMENTO SET NUMERO = '{novaInformacao}' WHERE ID_USUARIO = {IDusuario}")
                conn_DB.commit()
                print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")
                break
            except ValueError:
                print('Opção inválida! Digite novamente.....')
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

    def atualizar_endereco(self, conn_DB, IDusuario):
        print('\n1. Tipo de endereço\n2. Número\n3. Complemento\n4. Endereço com base em um novo CEP\n')

        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-4): '))
                if opcao == 1:
                    print('\nTipos de endereços disponíveis\n')
                    tEnderecos = ['Residencial', 'Corporativo']

                    for i in range(len(tEnderecos)):
                        print(str(i + 1) + ". " + tEnderecos[i])
                    print()
                    while True:
                        try:
                            novaInformacao = int(input('Digite a nova informação (1-2): '))
                            break
                        except ValueError:
                            print('Opção inválida! Digite novamente.....')

                    #Coletar ID do tipo de endereço no banco de dados
                    conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tEnderecos[novaInformacao - 1]}'")
                    idTipoEndereco = conn_DB.fetchval()

                    #Atualizando tipo de endereço do usuário
                    conn_DB.execute(f"UPDATE ENDERECO SET ID_TIPO_ENDERECO = {idTipoEndereco} WHERE ID_USUARIO = {IDusuario}")
                else:
                    if opcao == 2 or opcao == 3:
                        novaInformacao = input('Digite a nova informação: ').strip()
                        if opcao == 2:
                            coluna = 'NUMERO'
                        else:
                            coluna = 'COMPLEMENTO'
                        conn_DB.execute(f"UPDATE ENDERECO SET {coluna} = '{novaInformacao}' WHERE ID_USUARIO = {IDusuario}")
                    else:
                        caminho = Cadastro.Cadastro()
                        enderecoAtualizado = caminho.coletar_endereco()
                        if enderecoAtualizado == 0:
                            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
                            f'Por gentileza, tente mais tarde...')
                        else:
                            print(f'\nEndereço localizado:\n'
                                    f'Logradouro: {enderecoAtualizado["address"]}\n'
                                    f'Cidade: {enderecoAtualizado["city"]}\n'
                                    f'Estado: {enderecoAtualizado["state"]}\n'
                                    f'Bairro: {enderecoAtualizado["district"]}\n'
                                    f'CEP: {enderecoAtualizado["code"]}\n')

                            '''
                            Será validado em primeiro momento se o novo endereço já encontrasse cadastrado no banco
                            de dados. Caso esteja, será coletado apenas o ID do CEP, para associar ao usuário. Caso
                            contrário, o endereço será cadastrado no banco de dados e associado ao usuário
                            '''

                            #Validando se o CEP está cadastrado no banco de dados
                            conn_DB.execute(f"SELECT ID FROM CEP WHERE NUMERO = '{enderecoAtualizado['code']}'")
                            idCEP = conn_DB.fetchval()

                            if idCEP == None:
                                #Validando se UF já encontrasse cadastrada
                                conn_DB.execute(f"SELECT ID FROM UF WHERE SIGLA = '{enderecoAtualizado['state']}'")
                                IDuf = conn_DB.fetchval()

                                if IDuf == None:
                                    #Cadastrando UF
                                    conn_DB.execute("INSERT INTO UF VALUES (?)",
                                                    enderecoAtualizado['state'])

                                    #Coletando o ID da UF cadastrada
                                    conn_DB.execute("SELECT MAX(ID) FROM UF")
                                    IDuf = conn_DB.fetchval()

                                #Validando se cidade já encontrasse cadastrada
                                conn_DB.execute(f"SELECT ID FROM CIDADE WHERE NOME = '{enderecoAtualizado['city']}'")
                                IDcidade = conn_DB.fetchval()

                                if IDcidade == None:
                                    #Cadastrando Cidade
                                    conn_DB.execute("INSERT INTO CIDADE VALUES (?,?)",
                                                    IDuf, enderecoAtualizado['city'])

                                    #Coletando o ID da cidade cadastrada
                                    conn_DB.execute("SELECT MAX(ID) FROM CIDADE")
                                    IDcidade = conn_DB.fetchval()

                                #Validando se bairro já encontrasse cadastrada
                                conn_DB.execute(f"SELECT ID FROM BAIRRO WHERE NOME = '{enderecoAtualizado['district']}'")
                                IDbairro = conn_DB.fetchval()

                                if IDbairro == None:
                                    #Cadastrando Bairro
                                    conn_DB.execute("INSERT INTO BAIRRO VALUES (?,?)",
                                                    IDcidade, enderecoAtualizado['district'])

                                    #Coletando o ID do bairro cadastrado
                                    conn_DB.execute("SELECT MAX(ID) FROM BAIRRO")
                                    IDbairro = conn_DB.fetchval()

                                '''A API não encaminha o tipo e nome de logradouro já separado, desta forma,
                                o loop abaixo fará está separação e guardará dentro de duas variáveis.
                                '''
                                for i in range(len(enderecoAtualizado['address'])):
                                    if enderecoAtualizado['address'][i] == " ":
                                        Tipologradouro = enderecoAtualizado['address'][0:i]
                                        Nomelogradouro = enderecoAtualizado['address'][i + 1:]
                                        break

                                #Validando se tipo de logradouro já encontrasse cadastrada
                                conn_DB.execute(f"SELECT ID FROM TIPO_LOGRADOURO WHERE NOME = '{Tipologradouro}'")
                                IDtipo_logradouro = conn_DB.fetchval()

                                if IDtipo_logradouro == None:
                                    #Cadastrando Tipo de logradouro
                                    conn_DB.execute("INSERT INTO TIPO_LOGRADOURO VALUES (?,?)",
                                                    IDbairro, Tipologradouro)

                                    #Coletando o ID do tipo de logradouro
                                    conn_DB.execute("SELECT MAX(ID) FROM TIPO_LOGRADOURO")
                                    IDtipo_logradouro = conn_DB.fetchval()

                                #Cadastrando o Nome do logradouro
                                conn_DB.execute("INSERT INTO NOME_LOGRADOURO VALUES (?,?)",
                                                IDtipo_logradouro, Nomelogradouro)

                                #Cadastrando o CEP
                                conn_DB.execute("INSERT INTO CEP VALUES (?)",
                                                enderecoAtualizado['code'])

                                #Coletando o ID do CEP
                                conn_DB.execute("SELECT MAX(ID) FROM CEP")
                                idCEP = conn_DB.fetchval()
                            conn_DB.execute(f"UPDATE ENDERECO SET ID_CEP = {idCEP} WHERE ID_USUARIO = {IDusuario}")
                conn_DB.commit()
                print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")
                break
            except ValueError:
                print('Opção inválida! Digite novamente.....')
        pass

    def atualizar_telefone(self, conn_DB, IDusuario):
        print('\n1. Tipo de telefone\n2. DDD\n3. Número do telefone\n')

        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-3): '))
                if opcao == 1:
                    print('\nTipos de telefones disponíveis\n')
                    tTelefone = ["Particular", "Corporativo"]

                    for i in range(len(tTelefone)):
                        print(str(i + 1) + ". " + tTelefone[i])
                    print()
                    while True:
                        try:
                            novaInformacao = int(input('Digite a nova informação (1-2): '))
                            break
                        except ValueError:
                            print('Opção inválida! Digite novamente.....')

                    #Coletar ID do tipo de telefone no banco de dados
                    conn_DB.execute(f"SELECT ID FROM TIPO_TELEFONE WHERE NOME = '{tTelefone[novaInformacao - 1]}'")
                    idTipoTelefone = conn_DB.fetchval()

                    #Atualizando tipo de telefone do usuário
                    conn_DB.execute(f"UPDATE TELEFONE SET ID_TIPO_TELEFONE = {idTipoTelefone} WHERE ID_USUARIO = {IDusuario}")
                else:
                    novaInformacao = input('Digite a nova informação: ').strip()
                    if opcao == 2:
                        coluna = 'DDD'
                    else:
                        coluna = 'N_TELEFONE'
                    conn_DB.execute(f"UPDATE TELEFONE SET {coluna} = '{novaInformacao}' WHERE ID_USUARIO = {IDusuario}")
                conn_DB.commit()
                print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")
                break
            except ValueError:
                print('Opção inválida! Digite novamente.....')
        pass