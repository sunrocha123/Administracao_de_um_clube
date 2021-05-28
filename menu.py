from Associado import Cadastro, Atualizacao
from DB import configuracao

class Menu(object):

    def escolher_opcao_main(self):

        print(f'=================\nMENU\n=================\n'
            f'1. Inventário de associados\n'
            f'2. Mensalidades\n'
            f'3. Configurações\n')
        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-3): '))
                if opcao == 1:
                    self.escolher_opcao_inventario_associado()
                    break
                elif opcao == 2:
                    self.escolher_opcao_mensalidade()
                    break
                elif opcao == 3:
                    configuracao.cadastrar_informacoes()
                    break
                else:
                    print('Opção inválida! Digite novamente..')                   
            except ValueError:
                print('Opção inválida! Digite novamente..')
                
    def escolher_opcao_inventario_associado(self):
        print(f'\n1. Associar novo usuário\n'
            f'2. Alterar dados de usuário\n'
            f'3. Deletar usuário\n')

        while True:
            try:
                opcao = int(input("Digite a opção desejada (1-3): "))
                if opcao == 1:
                    caminho = Cadastro.Cadastro()
                    caminho.coletar_dados()
                    break
                elif opcao == 2:
                    caminho = Atualizacao.Atualizacao()
                    caminho.validar_cadastro()
                    break
                elif opcao == 3:
                    caminho.excluir_associado()
                    break
                else:
                    print("Opção inválida! Digite novamente...")
            except ValueError:
                print('Opção inválida! Digite novamente...')
                

    '''def escolher_opcao_mensalidade(self):
        print(f'\n1. Adicionar nova mensalidade\n'
            f'2. Alterar dados de uma mensalidade\n')

        caminho = Acoes_mensalidade.Mensalidades()

        while True:
            try:
                opcao = int(input('Digite a opção desejada (1-2): '))
                if opcao == 1:
                    caminho.cadastrar_nova_mensalidade()
                    break
                elif opcao == 2:
                    caminho.alterar_mensalidade()
                    break
                else:
                    print("Opção inválida! Digite novamente.....")    
            except ValueError:
                print('Opção inválida! Digite novamente.....')  '''

if __name__ == "__main__":
    print('Olá, bem-vindo ao nosso ADM do Club!\n')
    while True:
        caminho = Menu()
        caminho.escolher_opcao_main()
        realizar_mais_acoes = input("Digite qualquer coisa para sair ou 1 para realizar novas ações: ")

        if realizar_mais_acoes != '1':
                print('Obrigado por usar nossa ferramenta!')
                break
        
        print()
