'''
Esta classe guarda engines que ajudam com validação de cadastro,
ajuste de data e coleta de endereço na API dos correios
'''
from datetime import date, datetime
import requests

class engines(object):
    
    def validar_cadastro(self, conn_DB, numero_documento):

        '''
        Neste trecho, validaremos se o nº do documento informado já consta no banco de dados.
        Caso já esteja, não será feita a inclusão do novo usuário. Caso contrário, daremos
        sequência na inclusão.
        '''  
        conn_DB.execute(f"SELECT NUMERO FROM DOCUMENTO WHERE NUMERO = '{numero_documento}'")
        validacao = conn_DB.fetchval()
        if validacao == None:
            return 1
        else:
            return 0

    def coletar_endereco(self):
        try:           
            cep = input('Digite o CEP *: ').strip()
            print(f"\n{datetime.now().strftime('%H:%M:%S')}: "
                f"Conectando a API....") 
            response = requests.get(f'https://ws.apicep.com/cep/{cep}.json')
            print(f"{datetime.now().strftime('%H:%M:%S')}: "
                f"Conexão realizada com sucesso!")
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

        return 0

    def ajustarData(self):
        '''
        Está função tem como objetivo, arrumar a data informada pelo usuário
        no padrão YYYY-MM-DD para cadastro no banco de dados
        '''
        dataAjustada = ''

        dia = input('Digite o dia no formato DD: ')
        mes = input('Digite o mês no formato MM: ')
        ano = input('Digite o ano no formato YYYY: ')
        if dia != '' and mes != '' and ano != '':
            dataAjustada = ano + '-' + mes + '-' + dia
        return dataAjustada
