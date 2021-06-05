#Programa de Administração de um clube

#Foco do software: Gerenciar dados de associados de um club.

#Diagrama Database

<img src="diagrama banco de dados.png"/>

#Manual Software

#Menu

#Função: Interação com o usuário para coleta de dados/opções para manuseio (novas informações ou já existentes) no banco de dados do clube.

    #Opção inventário associado:
        #Neste campo, temos as seguintes ações:

            #1. Associar novo usuário - Cadastra um novo usuário no banco de dados do clube

                #Informações necessárias:
                    #- Nome (obrigatório)
                    #- Sobrenome (não obrigatório)
                    #- N_dependentes (não obrigatório)
                    #- Tipo de documento (obrigatório)
                    #- Número do documento (obrigatório)
                    #- Tipo de logradouro (obrigatório)
                    #- Nome do logradouro (obrigatório)
                    #- Complemento (não obrigatório)
                    #- Numero (não obrigatório)
                    #- Bairro (obrigatório)
                    #- CEP (não obrigatório)
                    #- Tipo de endereço (obrigatório)
                    #- Cidade (obrigatório)
                    #- Estado (obrigatório)


            #2. Alterar dados de associado - Atualização cadastral de um usuário já associado ao banco de dados do clube

                #Informações necessárias:
                    #- Número do documento do usuário (obrigatório)
                    #- Campo que terá a informação atualizada (endereço, documento...) - (obrigatório)
                    #- Subcampo com base no campo escolhido (obrigatório)
                        #Ex: Campo endereço > Subcampo: Tipo de endereço, nome do logradouro e etc.
                    #- Nova informação (obrigatório)

            #3. Deletar associado - Exclusão de um usuário do banco de dados

                #Informações necessárias:
                    #- Número do documento do usuário (obrigatório) 
                        #Com base nesta informação, todos os registros do usuário serão excluídos do banco de dados, inclusive as mensalidades que o mesmo possui vinculada em seu nome.

    #Opção mensalidade:
        #Neste campo, temos as seguintes ações:

            #1. Adicionar nova mensalidade - Cadastrar uma nova mensalidade de um determinado usuário no banco de dados

                #Informações necessárias:
                    #- Número do documento do usuário (obrigatório)
                    #- Data de vencimento (obrigatório)
                    #- Valor (obrigatório)
                    #- Data de pagamento (não obrigatório)

            #2. Alterar dados de uma mensalidade - Atualização cadastral de uma mensalidade já associada ao banco de dados

                #Informações necessárias:
                    #- Número do documento do usuário (obrigatório)
                    #- Campo que terá a informação atualizada (Data de vencimento, valor...) - (obrigatório)
                    #- Nova informação (obrigatório)

#Banco de dados - Se conectar com o banco de dados do clube que está no SQL Server da Microsoft, para realizar as ações solicitadas pelo usuário.

#Ações associado - Realizar cadastrado, atualização e exclusão de usuários no banco de dados

    #Cadastrado de usuários - Antes da inclusão, é realizada duas validações no banco de dados.

        #1. Validar se o nº do documento informado pelo usuário já está cadastrado no banco de dados. Caso esteja, não seguiremos com a inclusão. Será exibido para o usuário uma notificação sobre. Caso contrário, seguiremos com o processo de inclusão.

        #2. Validar se os campos tipo de documento, estado, cidade e tipo de endereço informados pelo usuário já estão cadastrados no banco de dados. Caso estejam, serão coletados os ID´s para inserção de outros dados que necessitam destas informações, evitando assim duplicidade de dados. Caso contrário, será feita a inclusão destes dados e posteriormente terão seus ID´s coletados para uso em outras inserção, caso necessário.

    #Atualização cadastral de associado - Antes da atualização, é realizada uma validação no banco de dados.

        #1. Validar se o nº do documento informado pelo usuário já está cadastrado no banco de dados. Caso esteja, coletaremos o ID do cliente, tendo em vista que é uma informação essencial para realizar as atualizações solicitadas. Caso contrário, não seguiremos com o processo. Será exibido para o usuário uma notificação sobre.

