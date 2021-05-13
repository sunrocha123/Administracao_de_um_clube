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

CREATE TABLE ENDERECO

(
	ID					INT				NOT NULL IDENTITY(1,1),
	ID_USUARIO			INT				NOT NULL,
	NUMERO				VARCHAR(10)		NULL,
	COMPLEMENTO			VARCHAR(20)		NULL,
	CEP					VARCHAR(10)		NULL,
	CONSTRAINT PK_ENDERECO PRIMARY KEY(ID),
	CONSTRAINT FK_ENDERECO_USUARIO FOREIGN KEY (ID_USUARIO)
		REFERENCES USUARIO(ID)
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
