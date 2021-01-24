import ler_informacoes
import excluir_associado
import alterar_informacoes
import escrever_arquivo

class Menu:

    def __init__(self):
        self.ler = ler_informacoes.Ler_informacoes()
        self.coleta_banco_de_dados = self.ler.leitura_dados()
        self.excluir = excluir_associado.Exclusao_associado()
        self.alterar = alterar_informacoes.Alteracao_de_informacoes()

    def adicionar_novos_associados(self, dados_do_novo_associado):
        associados_ja_cadastrados = self.coleta_banco_de_dados[0]
        banco_de_dados_associado_atualizado = associados_ja_cadastrados.append(dados_do_novo_associado)
        escrever_arquivo.escrever_arquivo(associados_ja_cadastrados, 'associados.txt')

    def adicionar_novas_mensalidades(self, dados_da_nova_mensalidade):
        mensalidades_ja_cadastradas = self.coleta_banco_de_dados[1]
        banco_de_dados_mensalidades_atualizado = mensalidades_ja_cadastradas.append(dados_da_nova_mensalidade)
        escrever_arquivo.escrever_arquivo(mensalidades_ja_cadastradas, 'mensalidades.txt')

    def excluir_associado(self, n_socio):
        self.excluir.excluir_associado(n_socio, self.coleta_banco_de_dados[0])

    def alterar_informacoes_associado(self, n_socio, local_de_alteracao, nova_informacao):
        self.alterar.alterar_informacoes(n_socio, local_de_alteracao, nova_informacao, self.coleta_banco_de_dados[0])
    
