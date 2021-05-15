USE ADM_Club;

CREATE TABLE USUARIO

(
	ID				INT				NOT NULL IDENTITY(1,1),
	NOME			VARCHAR(50)		NOT NULL,
	SOBRENOME		VARCHAR(100)	NULL,
	N_DEPENDENTES	INT				NULL,
	DTASSOCIACAO	DATETIME		NOT NULL,
	CONSTRAINT PK_USUARIO PRIMARY KEY(ID)
);

CREATE TABLE TIPO_TELEFONE

(
	ID			INT 		 NOT NULL IDENTITY(1,1),
	NOME 		VARCHAR(50)	 NOT NULL,
	DESCRICAO	VARCHAR(500) NULL,
	CONSTRAINT PK_TIPO_TELEFONE PRIMARY KEY (ID)
);

CREATE TABLE TELEFONE

(
	ID					INT			NOT NULL IDENTITY(1,1),
	ID_USUARIO			INT			NOT NULL,
	ID_TIPO_TELEFONE	INT			NOT NULL,
	DDD					VARCHAR(3)	NOT NULL,
	N_TELEFONE			VARCHAR(9)	NOT NULL,
	CONSTRAINT PK_TELEFONE PRIMARY KEY (ID),
	CONSTRAINT FK_TELEFONE_USUARIO FOREIGN KEY (ID_USUARIO)
		REFERENCES USUARIO(ID),
	CONSTRAINT FK_TELEFONE_TIPO_TELEFONE FOREIGN KEY (ID_TIPO_TELEFONE)
		REFERENCES TIPO_TELEFONE (ID)
);

CREATE TABLE TIPO_DOCUMENTO

(
	ID			INT				NOT NULL IDENTITY(1,1),
	NOME		VARCHAR(50)		NOT NULL,
	DESCRICAO	VARCHAR(500)	NULL,
	CONSTRAINT PK_TIPO_DOCUMENTO PRIMARY KEY(ID)
);

CREATE TABLE DOCUMENTO

(
	ID					INT			NOT NULL IDENTITY(1,1),
	ID_USUARIO			INT			NOT NULL,
	ID_TIPO_DOCUMENTO	INT			NOT NULL,
	NUMERO				VARCHAR(20)	NOT NULL,
	DTEMISSAO			DATE		NULL,
	VALIDADE			DATE		NULL,
	CONSTRAINT PK_DOCUMENTO PRIMARY KEY(ID),
	CONSTRAINT FK_DOCUMENTO_USUARIO FOREIGN KEY(ID_USUARIO)
		REFERENCES USUARIO(ID),
	CONSTRAINT FK_DOCUMENTO_TIPO_DOCUMENTO FOREIGN KEY(ID_TIPO_DOCUMENTO)
		REFERENCES TIPO_DOCUMENTO(ID)
);

CREATE TABLE TIPO_ENDERECO

(
	ID			INT 			NOT NULL IDENTITY(1,1),
	NOME		VARCHAR(50)		NOT NULL,
	DESCRICAO	VARCHAR(500)	NULL,
	CONSTRAINT PK_TIPO_ENDERECO PRIMARY KEY (ID)
);

CREATE TABLE UF

(
	ID			INT				NOT NULL IDENTITY(1,1),
	NOME		VARCHAR(50)		NOT NULL,
	SIGLA		VARCHAR(2)		NOT NULL,
	CONSTRAINT	PK_UF	PRIMARY KEY(ID)
);

CREATE TABLE CIDADE

(
	ID			INT				NOT NULL IDENTITY(1,1),
	ID_UF		INT				NOT NULL,
	NOME		VARCHAR(50)		NOT NULL,
	CONSTRAINT	PK_CIDADE	PRIMARY KEY (ID),
	CONSTRAINT FK_CIDADE_UF	FOREIGN KEY (ID_UF)
		REFERENCES	UF(ID)
);

CREATE TABLE ENDERECO

(
	ID					INT				NOT NULL IDENTITY(1,1),
	ID_USUARIO			INT				NOT NULL,
	ID_TIPO_ENDERECO	INT				NOT NULL,
	ID_CIDADE			INT				NOT NULL,
	TIPO_LOGRADOURO		VARCHAR(20)		NOT NULL,
	NOME_LOGRADOURO		VARCHAR(100)	NOT NULL,
	NUMERO				VARCHAR(6)		NULL,
	COMPLEMENTO			VARCHAR(20)		NULL,
	BAIRRO				VARCHAR(50)		NOT NULL,
	CEP					VARCHAR(8)		NULL,
	CONSTRAINT PK_ENDERECO PRIMARY KEY (ID),
	CONSTRAINT FK_ENDERECO_USUARIO FOREIGN KEY (ID_USUARIO)
		REFERENCES USUARIO(ID),
	CONSTRAINT FK_ENDERECO_TIPO_ENDERECO FOREIGN KEY (ID_TIPO_ENDERECO)
		REFERENCES TIPO_ENDERECO(ID),
	CONSTRAINT FK_ENDERECO_CIDADE FOREIGN KEY (ID_CIDADE)
		REFERENCES CIDADE(ID)
);

CREATE TABLE MENSALIDADE

(
	ID				INT				NOT NULL IDENTITY(1,1),
	ID_USUARIO		INT				NOT NULL,
	DTVENCIMENTO	DATE			NOT NULL,
	VALOR			DECIMAL(10,2)	NOT NULL,
	DTPAGAMENTO		DATE			NULL,
	CONSTRAINT PK_MENSALIDADE PRIMARY KEY(ID),
	CONSTRAINT FK_MENSALIDADE_USUARIO FOREIGN KEY(ID_USUARIO)
		REFERENCES USUARIO(ID)
);
