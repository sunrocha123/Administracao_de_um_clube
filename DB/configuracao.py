import pyodbc
from datetime import date, datetime
from DB import conexaoDB

def conectar_DB():
    return conexaoDB.conectar()

def cadastrar_informacoes():
    print(f'\n{datetime.now().strftime("%H:%M:%S")}: '
        f'Conectando ao banco de dados...')

    conn_DB = conectar_DB()

    if conn_DB == 0:
        print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
        f'Por gentileza, tente mais tarde...')

    else:
        Nometabelas = ['TIPO_TELEFONE', 'TIPO_DOCUMENTO', 'TIPO_ENDERECO']
        Dadostabelas = {"tipo_telefone": ["Particular", "Corporativo"], 
            "tipo_documento":['RG', 'CPF', 'Carteira de trabalho', 'Titulo de eleitor', 'CNH'],
            "tipo_endereco": ['Residencial', 'Corporativo']}

        print(f'{datetime.now().strftime("%H:%M:%S")}: '
            f'Inserindo dados no banco...')
        try:
            for i in range(len(Nometabelas)):
                for j in range(len(Dadostabelas[f'{Nometabelas[i].lower()}'])):
                    conn_DB.execute(f"INSERT INTO {Nometabelas[i]} (NOME) VALUES (?)",
                                    Dadostabelas[f'{Nometabelas[i].lower()}'][j])
                
                conn_DB.commit()
            
            print(f'{datetime.now().strftime("%H:%M:%S")}: '
                f'Dados inseridos com sucesso!')
        except Exception as error:
            print(f'{datetime.now().strftime("%H:%M:%S")}: '
                f'{error}\n')
            print(f'Desculpe, estamos com problemas técnicos em nossa ferramenta no momento\n'
            f'Por gentileza, tente mais tarde...')