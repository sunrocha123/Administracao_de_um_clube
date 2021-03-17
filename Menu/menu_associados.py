import ler_informacoes
import excluir_associado
import alterar_informacoes
import escrever_arquivo

class Menu:

    def __init__(self):
        self.ler = ler_informacoes.Ler_informacoes()
        self.excluir = excluir_associado.Exclusao_associado()
        self.alterar = alterar_informacoes.Alteracao_de_informacoes()

    def adicionar_novos_associados(self, dados_do_novo_associado):
        associados_ja_cadastrados = self.ler.leitura_dados('associados.txt')
        banco_de_dados_associado_atualizado = associados_ja_cadastrados.append(dados_do_novo_associado)
        escrever_arquivo.escrever_arquivo(associados_ja_cadastrados, 'associados.txt')
        criar_controle_mensalidades_novo_associado = escrever_arquivo.escrever_arquivo([],dados_do_novo_associado[0] + '.txt')

    def adicionar_novas_mensalidades(self, dados_da_nova_mensalidade):

        mensalidades_ja_cadastradas = self.ler.leitura_dados(dados_da_nova_mensalidade[0] + '.txt')
        banco_de_dados_mensalidades_atualizado = mensalidades_ja_cadastradas.append(dados_da_nova_mensalidade)
        escrever_arquivo.escrever_arquivo(mensalidades_ja_cadastradas, dados_da_nova_mensalidade[0] + '.txt')

    def excluir_associado(self, n_socio):
        self.excluir.excluir_associado(n_socio, self.ler.leitura_dados('associados.txt'))

    def alterar_informacoes_associado(self, n_socio, local_de_alteracao, nova_informacao):
        self.alterar.alterar_informacoes(n_socio, local_de_alteracao, nova_informacao, self.ler.leitura_dados('associados.txt'))
    
