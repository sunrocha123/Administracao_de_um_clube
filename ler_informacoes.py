class Ler_informacoes:
    def __init__(self):
        self.caminho_associados = 'associados.txt'
        self.caminho_mensalidades = 'mensalidades.txt'
    
    def leitura_dados(self):
        caminhos = [self.caminho_associados, self.caminho_mensalidades]
        banco_de_dados = [[],[]]

        for i in range(len(caminhos)):

            with open(caminhos[i],'r',encoding= 'utf-8') as put:
                for linha in put:
                    tamanho_linha = len(linha)
                    if linha[tamanho_linha - 1] == '\n':
                        banco_de_dados[i].append(linha[:tamanho_linha - 1].split(','))
                    else:
                        banco_de_dados[i].append(linha.split(','))

        return banco_de_dados
