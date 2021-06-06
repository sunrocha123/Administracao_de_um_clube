#Programa de Administração de um clube

#Foco do software: Gerenciar dados de associados de um club.

#Diagrama Database

<img src="DB/diagrama banco de dados.png"/>

#Manual Software

#Menu

#Função: Interação com o usuário para coleta de dados/opções para manuseio (novas informações ou já existentes) no banco de dados do clube. Além disso, possui uma opção de "configuração", aonde possui configurações essenciais, que precisam ser feitas após a criação do banco de dados.

    #Opção inventário associado:
        #Neste campo, temos as seguintes ações:

            #1. Associar novo associado - Cadastra um novo associado no banco de dados do clube

                #Informações necessárias:
                    #- Nome (obrigatório)
                    #- Sobrenome (não obrigatório)
                    #- N_dependentes (não obrigatório)
                    #- Tipo de documento (obrigatório)
                    #- Número do documento (obrigatório)
                    #- Data de emissão do documento (não obrigatório)
                    #- Validade do documento (não obrigatório)
                    #- Complemento (não obrigatório)
                    #- Numero (não obrigatório)
                    #- CEP (obrigatório)
                        --> Tendo o CEP, coletamos o endereço completo (estado, cidade, bairro, nome logradouro...) através de uma API que nos conecta aos correios.
                    #- Tipo de endereço (obrigatório)
                    #- Tipo de telefone (obrigatório)
                    #- DDD do telefone (obrigatório)
                    #- Número do telefone (obrigatório)


            #2. Manutenção cadastral de associado - Atualização ou inclusão de dados a um associado já existente no banco de dados do clube.

                #Informações necessárias:
                    #- Número do documento do associado (obrigatório)
                    #- Campo que terá a atualização ou inclusão de dados (endereço, documento...) - (obrigatório)
                    #- Nova informação (obrigatório)

            #3. Deletar associado - Exclusão de um associado do banco de dados

                #Informações necessárias:
                    #- Número do documento do associado (obrigatório) 
                        #Com base nesta informação, todos os registros do usuário serão excluídos do banco de dados, inclusive as mensalidades que o mesmo possui vinculada em seu nome.

    #Opção mensalidade:
        #Neste campo, temos as seguintes ações:

            #1. Adicionar nova mensalidade - Cadastrar uma nova mensalidade de um determinado associado no banco de dados

                #Informações necessárias:
                    #- Número do documento do associado (obrigatório)
                    #- Data de vencimento (obrigatório)
                    #- Valor (obrigatório)
                    #- Data de pagamento (não obrigatório)

            #2. Manutenção cadastral de uma mensalidade - Atualização de dados de uma mensalidade já associada ao banco de dados

                #Informações necessárias:
                    #- Número do documento do usuário (obrigatório)
                    #- Campo que terá a informação atualizada (Data de vencimento, valor...) - (obrigatório)
                    #- Nova informação (obrigatório)

