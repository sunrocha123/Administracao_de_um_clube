import menu_associados

class coleta_de_dados:

    def __init__(self):
        self.informacoes_necessarias_associado = ['nº sócio','nome','endereço','bairro','cidade','estado','nº dependentes','data de associação']

    def caminho(self):
        return menu_associados.Menu()

    def exibir_tela_inicial(self):
        print('\nOlá, bem-vindo ao administrador do clube :)\nNo que te ajudar?\n')
        opcao_acoes = ['1. Adicionar um novo associado','2. Adicionar uma nova mensalidade para determinado associado',
        '3. Alterar informações de um associado','4. Excluir um associado do sistema\n']
        
        for i in range(len(opcao_acoes)):
            print(opcao_acoes[i])

        while True:
            escolher_opcao = int(input('Digite a opção desejada: '))
            if escolher_opcao >= 1 and escolher_opcao <= 4:
                break
            else:
                print('Ops, opção inválida. Por gentileza, digite novamente!\n')

        if escolher_opcao == 1:
            self.novo_associado()
        else:
            if escolher_opcao == 2:
                self.nova_mensalidade()
            else:
                if escolher_opcao == 3:
                    self.alterar_informacoes_associado()
                else:
                    self.excluir_associado()


    def novo_associado(self):
        self.caminho().adicionar_novos_associados(self.coletar_dados(self.informacoes_necessarias_associado))

        print('\nO novo associado foi cadastrado com sucesso no sistema :)\n')

        while True:
            validar_se_deseja_cadastrar_mensalidade = input('Deseja cadastrar uma mensalidade no inventário do associado (Sim/Não)? ').upper()
            if validar_se_deseja_cadastrar_mensalidade == 'SIM':
                self.nova_mensalidade()
                break 
            else:
                if validar_se_deseja_cadastrar_mensalidade == 'NÃO':
                    break
                else:
                    print('Ops, opção inválida! Por gentileza, digite novamente (Sim/Não)\n')

    def nova_mensalidade(self):
        informacoes_necessarias_nova_mensalidade = ['nº sócio','data de vencimento','valor','data de pagamento']
        coletar_dados = self.coletar_dados(informacoes_necessarias_nova_mensalidade)
        validar_n_socio = self.validar_n_socio(coletar_dados[0])
        coletar_dados[0] = validar_n_socio

        self.caminho().adicionar_novas_mensalidades(coletar_dados)

        print('\nA mensalidade foi cadastrada com sucesso no banco de dados do associado :)\n')

    def alterar_informacoes_associado(self):
        n_socio = input('Digite o nº do sócio do associado: ').strip()
        validar_n_socio = self.validar_n_socio(n_socio)
        print('')

        for i in range(len(self.informacoes_necessarias_associado)):
            print(str(i + 1) + '. ' + (self.informacoes_necessarias_associado[i]).title())

        print('')

        while True:
            local_alteracao = input('Digite o número do local de alteração: ').strip()
            if int(local_alteracao) >= 1 and int(local_alteracao) <= 8:
                break
            else:
                print('Ops, local de alteração não localizado. Por gentileza, digite novamente!\n')

        nova_informacao = input('Digite a nova informação: ').strip().title()

        self.caminho().alterar_informacoes_associado(validar_n_socio, local_alteracao,nova_informacao)

        print('\nO cadastrado do associado foi atualizado com sucesso :)\n')

    def excluir_associado(self):

        n_socio = input('Digite o nº do sócio do associado: ').strip()
        self.caminho().excluir_associado(self.validar_n_socio(n_socio))

        print('\nO associado foi excluído do sistema com sucesso :)\n')

    def coletar_dados(self, informacoes_necessarias):
        dados_coletados = []
        for i in range(len(informacoes_necessarias)):
            coletar_dados = input('Digite o(a) ' + informacoes_necessarias[i] + ': ').strip().title()
            dados_coletados.append(coletar_dados)
        
        return dados_coletados

    def validar_n_socio(self, n_socio):

        while True:
            validacao = self.caminho().ler.leitura_dados('associados.txt')
            if validacao == []:
                print('Ops, nº de sócio não localizado no sistema. Por gentileza, verificar e digitar novamente.\n')
            else:
                for i in range(len(validacao)):
                    if n_socio == validacao[i][0]:
                        return n_socio

            print('Ops, nº de sócio não localizado no sistema. Por gentileza, verificar e digitar novamente.\n')             
            n_socio = input('Digite o nº do sócio do associado: ').strip()

def validar_novas_acoes_do_usuario():
    while True:
        validar_usuario_deseja_realizar_novas_operacoes = input('Deseja realizar mais alguma ação na ferramenta (Sim/Não)? ').upper()
        if validar_usuario_deseja_realizar_novas_operacoes == 'NÃO' or validar_usuario_deseja_realizar_novas_operacoes == 'SIM': 
            return validar_usuario_deseja_realizar_novas_operacoes
        else:
            print('Ops, opção inválida! Por gentileza, digite novamente (Sim/Não)\n')

while True:
    o = coleta_de_dados()
    o.exibir_tela_inicial()

    if validar_novas_acoes_do_usuario() == 'NÃO':
        print('Agradecemos por usar nossa ferramenta! :)')
        break


