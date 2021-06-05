from datetime import date, datetime
from DB import conexaoDB
from Associado import Mecanismo, Cadastro_associado

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
            Caso esteja cadastrado, coletaremos o ID do cliente para realizar as atualizações necessárias.

            '''
            print(f'Pontos de atenção:\n'
                    f'1. Para número de documento ou telefone, digitar sem espaço e traço\n'
                    f'2. Para o campo de CEP, digitar no formato 00000-000\n')
                    
            print('Antes de seguirmos com a atualização, precisamos realizar uma validação...')

            n_documento = input('Digite o número do documento do associado: ').strip()

            conn_DB.execute(f"SELECT ID_USUARIO FROM DOCUMENTO WHERE NUMERO = '{n_documento}'")
            IDassociado = conn_DB.fetchval()       

            if IDassociado == None:
                print(f'Usuário não localizado no banco de dados...\n'
                    f'Por gentileza, verificar...\n')
            
            else:
                '''
                Validar deseja atrelar um novo conjunto de dados ao associado
                ou atualizar um conjunto de dados já existente
                '''
                print(f'\n============================='
                        f'\nAÇÕES DISPONÍVEIS\n'
                        f'=============================\n')

                print(f'1. Adicionar novos dados a um associado existente\n'
                    f'2. Atualizar dados de um associado existente\n')

                while True:
                    try:
                        acaoDesejada = int(input('Digite a opção desejada: '))
                        if acaoDesejada < 1 or acaoDesejada > 2:
                            print("Opção inválida! Digite novamente....")
                        elif acaoDesejada == 1:
                            self.escolher_setor_novos_dados(conn_DB, IDassociado)
                            break
                        else:
                            self.escolher_setor_de_atualizacao(conn_DB, IDassociado, n_documento)
                            break
                    except ValueError:
                        print("Opção inválida! Digite novamente....")
        pass

    def escolher_setor_novos_dados(self, conn_DB, IDassociado):
        print('\n1. Telefone\n2. Documento\n3. Endereço\n')
        #Caminho para cadastro das informações
        caminho = Cadastro_associado.Cadastro()
        while True:
            try:
                opcaoDesejada = int(input('Digite a opção desejada para cadastrar novos dados: '))
                if opcaoDesejada < 1 or opcaoDesejada > 3:
                    print("Opção inválida! Digite novamente....")
                elif opcaoDesejada == 1:
                    caminho.cadastrar_telefone(IDassociado, conn_DB)
                    break
                elif opcaoDesejada == 2:
                    caminho.cadastrar_documento(conn_DB, IDassociado)
                    break
                else:
                    caminho.cadastrar_endereco(conn_DB, IDassociado)
                    break
            except ValueError:
                print("Opção inválida! Digite novamente....")

        conn_DB.commit()
        print(f"\n{datetime.now().strftime('%H:%M:%S')}: Informação cadastrada!\n")
        pass

    def escolher_setor_de_atualizacao(self, conn_DB, IDassociado, n_documento):
        print('\nÁreas de alteração\n\n1. Usuário\n2. Documento\n3. Telefone\n4. Endereço\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-4): '))
                if opcao == 1:
                    self.atualizar_usuario(conn_DB, IDassociado)
                    break
                elif opcao == 2:
                    self.atualizar_documento(conn_DB, IDassociado, n_documento)
                    break
                elif opcao == 3:
                    self.atualizar_telefone(conn_DB, IDassociado)
                    break
                elif opcao == 4:
                    self.atualizar_endereco(conn_DB, IDassociado)
                    break
                else:
                    print("Opção inválida! Digite novamente....")    
            except ValueError:
                print('Opção inválida! Digite novamente....')
        conn_DB.commit()
        print(f"{datetime.now().strftime('%H:%M:%S')}: Informação atualizada!\n")         
        pass

    def atualizar_usuario(self, conn_DB, IDassociado):
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
                    conn_DB.execute(f"UPDATE USUARIO SET N_DEPENDENTES = {novaInformacao} WHERE ID = {IDassociado}")
                    break
                elif opcao == 1 or opcao == 2:
                    novaInformacao = input('Digite a nova informação: ').lower().strip()
                    if opcao == 1:
                        coluna = 'NOME'
                    elif opcao == 2:
                        coluna = 'SOBRENOME'
                    conn_DB.execute(f"UPDATE USUARIO SET {coluna} = '{novaInformacao}' WHERE ID = {IDassociado}")
                    break
                else:
                    print('Opção inválida! Digite novamente.....')
            except ValueError:
                print('Opção inválida! Digite novamente.....')

    def atualizar_documento(self, conn_DB, IDassociado, n_documento):
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
                            if novaInformacao < 1 or novaInformacao > 5:
                                print('Opção inválida! Digite novamente.....')
                            else:
                                break
                        except ValueError:
                            print('Opção inválida! Digite novamente.....')

                    #Coletar ID do tipo de documento no banco de dados
                    conn_DB.execute(f"SELECT ID FROM TIPO_DOCUMENTO WHERE NOME = '{tdocumentos[novaInformacao - 1]}'")
                    idTipoDocumento = conn_DB.fetchval()

                    #Atualizando tipo de documento do usuário
                    conn_DB.execute(f"UPDATE DOCUMENTO SET ID_TIPO_DOCUMENTO = {idTipoDocumento} WHERE ID_USUARIO = {IDassociado} AND NUMERO = '{n_documento}'")
                    break
                elif opcao == 3 or opcao == 4:
                    dataAtualizada = self.conectar_engines().ajustarData()
                    if opcao == 3:
                        conn_DB.execute(f"UPDATE DOCUMENTO SET DTEMISSAO = '{dataAtualizada}' WHERE ID_USUARIO = {IDassociado} AND NUMERO = '{n_documento}'")
                    else:
                        conn_DB.execute(f"UPDATE DOCUMENTO SET VALIDADE = '{dataAtualizada}' WHERE ID_USUARIO = {IDassociado} AND NUMERO = '{n_documento}'")
                    break
                elif opcao == 2:
                    novaInformacao = input('Digite a nova informação: ').strip()
                    conn_DB.execute(f"UPDATE DOCUMENTO SET NUMERO = '{novaInformacao}' WHERE ID_USUARIO = {IDassociado} AND NUMERO = '{n_documento}'")
                    break
                else:
                    print('Opção inválida! Digite novamente.....')
            except ValueError:
                print('Opção inválida! Digite novamente.....')
        pass

    def atualizar_endereco(self, conn_DB, IDassociado):
        print('\n1. Tipo de endereço\n2. Número\n3. Complemento\n4. Endereço com base em um novo CEP\n')

        while True:

            CEPcadastrado = input('Digite o CEP do endereço que deseja atualizar: ')
            conn_DB.execute(f"SELECT ID_CEP FROM ENDERECO INNER JOIN CEP ON ENDERECO.ID_CEP = CEP.ID WHERE ID_USUARIO = {IDassociado} AND CEP.NUMERO = '{CEPcadastrado}'")
            IDcep = conn_DB.fetchval()  

            if IDcep == None:
                print('CEP não localizado...\nPor gentileza, digitar novamente!\n')
        
            else:
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
                                    if novaInformacao < 1 or novaInformacao > 2:
                                        print('Opção inválida! Digite novamente.....')
                                    else:
                                        break
                                except ValueError:
                                    print('Opção inválida! Digite novamente.....')

                            #Coletar ID do tipo de endereço no banco de dados
                            conn_DB.execute(f"SELECT ID FROM TIPO_ENDERECO WHERE NOME = '{tEnderecos[novaInformacao - 1]}'")
                            idTipoEndereco = conn_DB.fetchval()

                            #Atualizando tipo de endereço do usuário
                            conn_DB.execute(f"UPDATE ENDERECO SET ID_TIPO_ENDERECO = {idTipoEndereco} WHERE ID_USUARIO = {IDassociado} AND ID_CEP = {IDcep}")
                            break
                        elif opcao == 2 or opcao == 3:
                            novaInformacao = input('Digite a nova informação: ').strip()
                            if opcao == 2:
                                coluna = 'NUMERO'
                            else:
                                coluna = 'COMPLEMENTO'
                            conn_DB.execute(f"UPDATE ENDERECO SET {coluna} = '{novaInformacao}' WHERE ID_USUARIO = {IDassociado} AND ID_CEP = {IDcep}")
                            break
                        elif opcao == 4:
                            caminho = Cadastro_associado.Cadastro()
                            caminho.cadastrar_endereco(conn_DB, IDassociado)
                            break
                        else:
                            print('Opção inválida! Digite novamente.....')
                    except ValueError:
                        print('Opção inválida! Digite novamente.....')
                break
        pass

    def atualizar_telefone(self, conn_DB, IDassociado):
        print('\n1. Tipo de telefone\n2. DDD\n3. Número do telefone\n')

        ddd = input('Digite o DDD do telefone cadastrado: ')
        nTelefone = input('Digite o número do telefone cadastrado: ')

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
                    conn_DB.execute(f"UPDATE TELEFONE SET ID_TIPO_TELEFONE = {idTipoTelefone} WHERE ID_USUARIO = {IDassociado} AND DDD = '{ddd}' AND N_TELEFONE = '{nTelefone}'")
                    break
                elif opcao == 2 or opcao == 3:
                    novaInformacao = input('Digite a nova informação: ').strip()
                    if opcao == 2:
                        coluna = 'DDD'
                    else:
                        coluna = 'N_TELEFONE'
                    conn_DB.execute(f"UPDATE TELEFONE SET {coluna} = '{novaInformacao}' WHERE ID_USUARIO = {IDassociado} AND DDD = '{ddd}' AND N_TELEFONE = '{nTelefone}'")
                    break
                else:
                    print('Opção inválida! Digite novamente.....')
            except ValueError:
                print('Opção inválida! Digite novamente.....')
        pass