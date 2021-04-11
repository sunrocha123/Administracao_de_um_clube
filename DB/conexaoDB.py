from datetime import date, datetime
import pyodbc

def conectar():
    try:
        conexao = pyodbc.connect("Driver={SQL Server};"
                              "Server=NVT-847\SQLEXPRESS;"
                              "Database=ADM_Club;"
                              "UID=sa;"
                              "PWD=sa;")

        conector = conexao.cursor()
        print(f'{datetime.now().strftime("%H:%M:%S")}: Conexão realizada com sucesso!')
        return conector

    except Exception as error:
        print(f'{datetime.now().strftime("%H:%M:%S")}: Falha na conexão com o banco de dados!\n')
        return 0
        