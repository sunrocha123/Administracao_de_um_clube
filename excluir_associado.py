import escrever_arquivo

class Exclusao_associado:

    def excluir_associado(self, n_socio, banco_de_dados_associados):
        for i in range(len(banco_de_dados_associados)):
            if n_socio == banco_de_dados_associados[i][0]:
                del(banco_de_dados_associados[i])
                break

        escrever_arquivo.escrever_arquivo(banco_de_dados_associados, 'associados.txt')

                  