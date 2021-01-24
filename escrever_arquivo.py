def escrever_arquivo(banco_de_dados, caminho):

    with open(caminho,'w', encoding='utf-8') as get:
        for i in range (len(banco_de_dados)):
            for j in range(len(banco_de_dados[0])):
                if j == len(banco_de_dados[0]) - 1:
                    get.write(banco_de_dados[i][j] + '\n')
                else:
                    get.write(banco_de_dados[i][j] + ',')