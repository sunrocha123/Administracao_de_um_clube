from datetime import date, datetime
from Acoes import DB
import pyodbc

class Menu(object):

    def escolher_opcao_main(self):
        print(f'\n=================\nMENU\n=================\n'
            f'1. Inventário de associados\n'
            f'2. Mensalidades\n')
        
        while True:
            opcao = int(input('Digite a opção desejada (1-2): '))
            if opcao == 1:
                self.escolher_opcao_inventario_associado()
            elif opcao == 2:
                self.escolher_opcao_mensalidade()
            else:
                print('Opção inválida! Digite novamente...')

    def escolher_opcao_inventario_associado(self):
        print(f'\n1. Associar novo usuário\n'
            f'2. Alterar dados de associado\n'
            f'3. Excluir associado\n')
        pass

    def escolher_opcao_mensalidade(self):
        print(f'\n1. Adicionar nova mensalidade\n'
            f'2. Alterar dados de uma mensalidade\n'
            f'3. Excluir mensalidade\n')        
        pass

if __name__ == "__main__":
    print(f'Olá, bem-vindo ao nosso ADM do Club!\n'
        f'Estamos preparando o ambiente para você...\n')

    print(f'{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao Database...')

    conector_DB = DB.conectar()

    if conector_DB == 0:
        print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde... :(')
    else:
        print('\nTudo pronto, partiu!!!!!')
        caminho = Menu()
        caminho.escolher_opcao_main()

