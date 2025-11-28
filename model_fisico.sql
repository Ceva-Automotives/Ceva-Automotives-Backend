
CREATE TABLE localizacoes (
	id SERIAL NOT NULL, 
	nome VARCHAR(200) NOT NULL, 
	endereco VARCHAR(500) NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
)

;

CREATE TABLE usuarios (
	id SERIAL NOT NULL, 
	nome VARCHAR(200) NOT NULL, 
	email VARCHAR(200) NOT NULL, 
	senha VARCHAR(255) NOT NULL, 
	telefone VARCHAR(20), 
	"dataCadastro" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	tipo VARCHAR(50) NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
)

;

CREATE TABLE admins (
	id INTEGER NOT NULL, 
	cargo VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES usuarios (id)
)

;

CREATE TABLE carros (
	id SERIAL NOT NULL, 
	placa VARCHAR(10) NOT NULL, 
	marca VARCHAR(100) NOT NULL, 
	modelo VARCHAR(100) NOT NULL, 
	ano INTEGER NOT NULL, 
	cor VARCHAR(50) NOT NULL, 
	"precoDia" FLOAT NOT NULL, 
	categoria VARCHAR(100) NOT NULL, 
	status statuscarro NOT NULL, 
	descricao VARCHAR(500), 
	disponivel BOOLEAN NOT NULL, 
	destaque BOOLEAN NOT NULL, 
	"localizacaoId" INTEGER, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (placa), 
	FOREIGN KEY("localizacaoId") REFERENCES localizacoes (id)
)

;

CREATE TABLE clientes (
	id INTEGER NOT NULL, 
	cnh VARCHAR(20) NOT NULL, 
	cpf VARCHAR(14) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES usuarios (id), 
	UNIQUE (cnh), 
	UNIQUE (cpf)
)

;

CREATE TABLE avaliacoes (
	id SERIAL NOT NULL, 
	nota INTEGER NOT NULL, 
	comentario TEXT, 
	data TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"clienteId" INTEGER NOT NULL, 
	"carroId" INTEGER NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("clienteId") REFERENCES clientes (id), 
	FOREIGN KEY("carroId") REFERENCES carros (id)
)

;

CREATE TABLE dashboards (
	id SERIAL NOT NULL, 
	nome VARCHAR(200) NOT NULL, 
	"adminId" INTEGER NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE ("adminId"), 
	FOREIGN KEY("adminId") REFERENCES admins (id)
)

;

CREATE TABLE reservas (
	id SERIAL NOT NULL, 
	"dataRetirada" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"dataDevolucao" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"valorTotal" FLOAT NOT NULL, 
	status statusreserva NOT NULL, 
	"clienteId" INTEGER NOT NULL, 
	"carroId" INTEGER NOT NULL, 
	"localizacaoRetiradaId" INTEGER NOT NULL, 
	"localizacaoDevolucaoId" INTEGER NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("clienteId") REFERENCES clientes (id), 
	FOREIGN KEY("carroId") REFERENCES carros (id), 
	FOREIGN KEY("localizacaoRetiradaId") REFERENCES localizacoes (id), 
	FOREIGN KEY("localizacaoDevolucaoId") REFERENCES localizacoes (id)
)

;

CREATE TABLE metricas (
	id SERIAL NOT NULL, 
	nome VARCHAR(200) NOT NULL, 
	valor VARCHAR(200) NOT NULL, 
	tipo VARCHAR(100) NOT NULL, 
	"dashboardId" INTEGER NOT NULL, 
	"criadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	"atualizadoEm" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("dashboardId") REFERENCES dashboards (id)
)

;
