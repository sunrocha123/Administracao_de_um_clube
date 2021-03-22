from Acoes import Acoes_associado, Acoes_mensalidade

class Menu(object):

    def escolher_opcao_main(self):

        while True:
            print(f'=================\nMENU\n=================\n'
                f'1. Inventário de associados\n'
                f'2. Mensalidades\n')
        
            opcao = int(input('Digite a opção desejada (1-2): '))
            if opcao == 1:
                self.escolher_opcao_inventario_associado()
            elif opcao == 2:
                self.escolher_opcao_mensalidade()
            else:
                print('Opção inválida! Digite novamente...')

            realizar_mais_acoes = input("Deseja realizar outras ações (S/N)? ").title().strip()
            print()

            if realizar_mais_acoes == "N" or realizar_mais_acoes == "Não" or realizar_mais_acoes == "Nao":
                break

    def escolher_opcao_inventario_associado(self):
        print(f'\n1. Associar novo usuário\n'
            f'2. Alterar dados de associado\n'
            f'3. Excluir associado\n')
        
        opcao = self.retornar_escolhaOpcao()
        caminho = Acoes_associado.Associados()
        if opcao == 1:
            caminho.cadastrar_novo_associado()
            pass
        elif opcao == 2:
            pass
        else:
            caminho.excluir_associado()
            pass
        pass

    def escolher_opcao_mensalidade(self):
        print(f'\n1. Adicionar nova mensalidade\n'
            f'2. Alterar dados de uma mensalidade\n'
            f'3. Excluir mensalidade\n')

        opcao = self.retornar_escolhaOpcao()

        if opcao == 1:
            pass
        elif opcao == 2:
            pass
        else:
            pass    
        pass

    def retornar_escolhaOpcao(self):
        while True:
            opcao = int(input('Digite a opção desejada (1-3): '))
            if opcao >= 1 and opcao <= 3:
                return opcao
            else:
                print('Opção inválida! Digite novamente...')        

if __name__ == "__main__":
    print('Olá, bem-vindo ao nosso ADM do Club!\n')
    caminho = Menu()
    caminho.escolher_opcao_main()

