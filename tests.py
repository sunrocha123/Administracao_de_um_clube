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
    novas_mensalidades = [['001','12/09/2020','200','21/09/2020'],
    ['002','25/03/2020','350','01/04/2020'],
    ['003','05/05/2020','1000','15/05/2020']]

    for i in range(len(novas_mensalidades)):
        caminho().adicionar_novas_mensalidades(novas_mensalidades[i])

def test_excluir_associado():
    caminho().excluir_associado('001')

def test_alterar_informacoes_associado():
    caminho().alterar_informacoes_associado('002','3','Avenida Brigadeiro Faria Lima')


