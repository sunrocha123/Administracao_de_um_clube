import escrever_arquivo

class Alteracao_de_informacoes:

    def alterar_informacoes(self, n_socio, local_de_alteracao, nova_informacao, banco_de_dados_associados):
        for i in range(len(banco_de_dados_associados)):
            if n_socio == banco_de_dados_associados[i][0]:
                banco_de_dados_associados[i][int(local_de_alteracao) - 1] = nova_informacao
                break

        escrever_arquivo.escrever_arquivo(banco_de_dados_associados, 'associados.txt')
