class Ler_informacoes:
  
    def leitura_dados(self, caminho):

        banco_de_dados = []

        with open(caminho,'r',encoding= 'utf-8') as put:
            for linha in put:
                tamanho_linha = len(linha)
                if linha[tamanho_linha - 1] == '\n':
                    banco_de_dados.append(linha[:tamanho_linha - 1].split(','))
                else:
                    banco_de_dados.append(linha.split(','))

        return banco_de_dados
