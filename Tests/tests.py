import menu_associados

def caminho():
    return menu_associados.Menu()

def test_novo_associado():
    novos_associados = [['001','Judson Santana','Rua Eng. Hugo Takahashi','Raposo Tavares','São Paulo','São Paulo','3','12/09/2018'],
    ['002','Ana Caroline','Rua Teodoro Sampaio','Pinheiros','São Paulo','São Paulo','2','06/01/2017'],
    ['003','João Pedro','Rua Eng. Hugo Takahashi','Raposo Tavares','São Paulo','São Paulo','8','23/11/2016']]

    for i in range(len(novos_associados)):
        caminho().adicionar_novos_associados(novos_associados[i])

def test_nova_mensalidade():

    mensalidades_jan_a_abr = [[['001','05/01/2020','150',''],['002','15/01/2020','100','12/01/2020'],['003','18/01/2020','400','21/01/2020']],
    [['001','05/02/2020','180',''],['002','15/02/2020','100','11/02/2020'],['003','18/02/2020','420','17/02/2020']],
    [['001','05/03/2020','245',''],['002','15/03/2020','100','02/03/2020'],['003','18/03/2020','400','16/03/2020']],
    [['001','05/04/2020','360',''],['002','15/04/2020','80','12/04/2020'],['003','18/04/2020','390','16/04/2020']]]

    for i in range(len(mensalidades_jan_a_abr)):
        for j in range(len(mensalidades_jan_a_abr[0])):
            caminho().adicionar_novas_mensalidades(mensalidades_jan_a_abr[i][j])

def test_excluir_associado():
    caminho().excluir_associado('001')

def test_alterar_informacoes_associado():
    caminho().alterar_informacoes_associado('002','3','Avenida Brigadeiro Faria Lima')

test_novo_associado()
test_nova_mensalidade()

