import menu_associados

class coleta_de_dados:

    def __init__(self):
        self.informacoes_necessarias_associado = ['nº sócio','nome','endereço','bairro','cidade','estado','nº dependentes','data de associação']

    def caminho(self):
        return menu_associados.Menu()

    def exibir_tela_inicial(self):
        print('Olá, bem-vindo ao administrador do clube :)\nNo que te ajudar?\n')
        opcao_acoes = ['1. Adicionar um novo associado','2. Adicionar uma nova mensalidade para determinado associado',
        '3. Alterar informações de um associado','4. Excluir um associado do sistema\n']
        
        for i in range(len(opcao_acoes)):
            print(opcao_acoes[i])

        escolher_opcao = int(input('Digite a opção desejada: '))

        if int(escolher_opcao) == 1:
            self.novo_associado()
        else:
            if int(escolher_opcao) == 2:
                self.nova_mensalidade()
            else:
                if int(escolher_opcao) == 3:
                    self.alterar_informacoes_associado()
                else:
                    self.excluir_associado()


    def novo_associado(self):
        self.caminho().adicionar_novos_associados(self.coletar_dados(self.informacoes_necessarias_associado))

        print('\nO novo associado foi cadastrado com sucesso no sistema :)')

    def nova_mensalidade(self):
        informacoes_necessarias_nova_mensalidade = ['nº sócio','data de vencimento','valor','data de pagamento']
        self.caminho().adicionar_novas_mensalidades(self.coletar_dados(informacoes_necessarias_nova_mensalidade))

        print('\nA mensalidade foi cadastrada com sucesso no banco de dados do associado :)')

    def alterar_informacoes_associado(self):
        n_socio = input('Digite o nº do sócio do associado: ').strip()
        print('')

        for i in range(len(self.informacoes_necessarias_associado)):
            print(str(i + 1) + '. ' + (self.informacoes_necessarias_associado[i]).title())

        print('')

        local_alteracao = input('Digite o número do local de alteração: ').strip()
        nova_informacao = input('Digite a nova informação: ').strip().title()

        self.caminho().alterar_informacoes_associado(n_socio,local_alteracao,nova_informacao)

        print('\nO cadastrado do associado foi atualizado com sucesso :)')

    def excluir_associado(self):
        n_socio = input('Digite o nº do sócio do associado: ').strip().title()
        self.caminho().excluir_associado(n_socio)

        print('\nO associado foi excluído do sistema com sucesso :)')

    def coletar_dados(self, informacoes_necessarias):
        dados_coletados = []
        for i in range(len(informacoes_necessarias)):
            coletar_dados = input('Digite o(a) ' + informacoes_necessarias[i] + ': ').strip().title()
            dados_coletados.append(coletar_dados)
        
        return dados_coletados

o = coleta_de_dados()
o.exibir_tela_inicial()