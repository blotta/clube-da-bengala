
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS beneficiarios;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

DROP TABLE IF EXISTS equip_sizes;
DROP TABLE IF EXISTS equip_models;
DROP TABLE IF EXISTS equip_types;
DROP TABLE IF EXISTS equipamentos_status;
DROP TABLE IF EXISTS equipamentos;

DROP TABLE IF EXISTS emprestimos_status;
DROP TABLE IF EXISTS emprestimos;


CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  mobilenumber TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL
);

CREATE TABLE addresses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  zipcode TEXT NOT NULL,
  street TEXT NOT NULL,
  number INTEGER NOT NULL,
  complement TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  active INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE beneficiarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  responsavel_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  dataNascimento DATE NOT NULL,
  altura REAL NULL,
  peso REAL NULL,
  nrCalcado INTEGER NULL,
  active INTEGER NOT NULL,

  FOREIGN KEY (responsavel_id) REFERENCES users (id)
);

CREATE TABLE roles (
  id INTEGER PRIMARY KEY,
  role TEXT UNIQUE NOT NULL
);

INSERT INTO roles (id, role) VALUES
    (0, 'Colaborador')
  , (1, 'Beneficiario')
  , (2, 'Doador');


CREATE TABLE user_roles (
  user_id INTEGER NOT NULL,
  role_id TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (role_id) REFERENCES roles (id)
);


-----------------
-- EQUIP TYPES --
-----------------
CREATE TABLE equip_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
INSERT INTO equip_types (id, name) VALUES
    (4,  'Andador')
  , (8,  'Bengala')
  , (2,  'Cadeira de Rodas')
  , (3,  'Cadeira de Banho')
  , (1,  'Cama Hospitalar')
  , (20, 'Colchão')
  , (5,  'Muleta Axilar')
  , (6,  'Muleta Canadense (de braço)')
  , (9,  'Bota Imobilizadora')
  , (18, 'Colar Cervical')
  , (15, 'Tipoia')
  , (7,  'Imobilizador de Joelho')
  , (27, 'Joelheira')
  , (19, 'Imobilizador Pé / Tornozelo');


------------------
-- EQUIP MODELS --
------------------
CREATE TABLE equip_models (
  equip_type_id INTEGER,
  model_num INTEGER,
  name TEXT NOT NULL,
  image TEXT NULL,
  PRIMARY KEY (equip_type_id, model_num),
  FOREIGN KEY (equip_type_id) REFERENCES equip_types (id)
);
INSERT INTO equip_models (equip_type_id, model_num, name, image) VALUES
--    (4,  1, 'Articulado')
--  , (4,  4, 'Especial Infantil')
--  , (4,  2, 'Especial Adulto')
--  , (8,  1, 'Madeira')
--  , (8,  2, 'Alumínio')
--  , (8,  4, 'Quatro Pontos')
--  , (8,  3, 'Deficiente Visual')
--  , (2,  1, 'Standard Adulto')
--  , (2,  2, 'Especial Adulto')
--  , (2,  4, 'Adaptada Infantil')
--  , (3,  1, 'Standard Adulto')
--  , (3,  2, 'Especial Adulto')
--  , (1,  1, 'Manual')
--  , (1,  2, 'Motorizada')
--  , (20, 1, 'Caixa de Ovo')
--  , (5,  1, 'Alumínio (par) Adulto')
--  , (5,  2, 'Madeira (par) Adulto')
--  , (5,  3, 'Alumínio (par) Infantil')
--  , (6,  3, 'Par Adulto')
--  , (6,  4, 'Par Infantil')
--  , (9,  1, 'Robofoot Curta')
--  , (9,  2, 'Robofoot Longa')
--  , (18, 1, 'Espuma')
--  , (15, 1, 'Padrão')
--  , (7,  1, 'Fixo')
--  , (27, 1, 'Padrão')
--  , (19, 1, 'Padrão')
--  , (25, 1, 'Padrão')
--  , (11, 1, 'Padrão');

   (4, 1, 'Articulado', '04-01.jpg')
 , (4, 4, 'Especial Infantil', '04-04.jpg')
 , (4, 2, 'Especial adulto', '04-02.jpg')
 , (8, 1, 'Madeira', '08-00.jpg')
 , (8, 2, 'Alumínio', '08-00.jpg')
 , (8, 4, 'Quatro Pontos', '08-04.jpg')
 , (8, 3, 'Deficiente Visual', '08-03.jpg')
 , (2, 1, 'Standard Adulto', '02-01.jpg')
 , (2, 2, 'Especial Adulto', '02-02.jpg')
 , (2, 4, 'Adaptada Infantil', '02-04.jpg')
 , (3, 1, 'Standard Adulto', '03-01.jpg')
 , (3, 2, 'Especial Adulto', '03-02.jpg')
 , (1, 1, 'Manual', '01-01.jpg')
 , (1, 2, 'Motorizada', '01-02.jpg')
 , (20, 1, 'Caixa de Ovo', '20-00.jpg')
 , (5, 1, 'Alumínio (par) Adulto', '05-01.jpg')
 , (5, 2, 'Madeira (par) Adulto', '05-02.jpg')
 , (5, 3, 'Alumínio (par) Infantil', '05-03.jpg')
 , (6, 3, 'Par Adulto', '06-03.jpg')
 , (6, 4, 'Par Infantil', '06-04.jpg')
 , (9, 1, 'Robofoot Curta', '09-00.jpg')
 , (9, 2, 'Robofoot Longa', '09-00.jpg')
 , (18, 1, 'Espuma', '18-00.jpg')
 , (15, 1, 'Padrão', '15-00.jpg')
 , (7, 1, 'Fixo', '07-00.jpg')
 , (27, 1, 'Padrão', '27-00.jpg')
 , (19, 1, 'Padrão', '19-00.jpg')
 , (25, 1, 'Padrão', '25-00.jpg')
 , (11, 1, 'Padrão', '11-00.jpg');

------------------
-- EQUIP SIZES --
------------------
CREATE TABLE equip_sizes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  equip_type_id INTEGER,
  equip_model_num INTEGER,
  desc TEXT NOT NULL,
  FOREIGN KEY (equip_type_id) REFERENCES equip_types (id)
);
INSERT INTO equip_sizes (equip_type_id, equip_model_num, desc) VALUES
    (2, 2, 'Até 120kg')

  , (5, 1, 'P - 1,37m a 1,57m')
  , (5, 1, 'M - 1,57m a 1,78m')
  , (5, 1, 'G - 1,78m a 1,98m')

  , (5, 2, 'P - 1,37m a 1,57m')
  , (5, 2, 'M - 1,57m a 1,78m')
  , (5, 2, 'G - 1,78m a 1,98m')

  , (5, 3, 'Único - Entre 1,22m e 1,37m')

  , (6, 3, 'P - 1,37m a 1,57m')
  , (6, 3, 'M - 1,57m a 1,78m')
  , (6, 3, 'G - 1,78m a 1,98m')

  , (9, 1, 'P')
  , (9, 1, 'M')
  , (9, 1, 'G')

  , (9, 2, 'P')
  , (9, 2, 'M')
  , (9, 2, 'G')

  , (7, 1, 'P - 50cm')
  , (7, 1, 'M - 60cm')
  , (7, 1, 'G - 70cm');




CREATE TABLE equipamentos_status (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

INSERT INTO equipamentos_status (id, name) VALUES
    (0, 'Disponível')
  , (1, 'Emprestado')
  , (2, 'Em Manutenção')
  , (3, 'Indisponível')
  , (4, 'Reservado');

CREATE TABLE equipamentos (
  id INTEGER PRIMARY KEY,
  status INTEGER NOT NULL,
  equip_type INTEGER NOT NULL,
  equip_model INTEGER NOT NULL,
  equip_size INTEGER NULL,
  obs TEXT NULL,

  FOREIGN KEY (equip_type, equip_model) REFERENCES equip_models (equip_type_id, equip_model_num)
);

-----------------
-- EMPRESTIMOS --
-----------------

CREATE TABLE emprestimos_status (
  id INTEGER PRIMARY KEY,
  status TEXT UNIQUE NOT NULL
);

INSERT INTO emprestimos_status (id, status) VALUES
    (0, 'Solicitado')
  , (1, 'Aprovado')
  , (2, 'Negado')
  , (3, 'Cancelado')
  , (4, 'Emprestado');


CREATE TABLE emprestimos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status INTEGER NOT NULL,
  solicitante_id INTEGER NOT NULL,
  beneficiario_id INTEGER NOT NULL,
  address_id INTEGER NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  motivo TEXT NOT NULL,
  obs TEXT NULL,
  equip_type INTEGER NOT NULL,
  equip_model INTEGER NOT NULL,
  equip_size INTEGER NULL,
  equip_id INTEGER NULL,

  FOREIGN KEY (solicitante_id) REFERENCES users (id),
  FOREIGN KEY (beneficiario_id) REFERENCES beneficiarios (id),
  FOREIGN KEY (address_id) REFERENCES addresses (id),
  FOREIGN KEY (status) REFERENCES emprestimos_status (id)
  FOREIGN KEY (equip_id) REFERENCES equipamentos (id)
  FOREIGN KEY (equip_type, equip_model) REFERENCES equip_models (equip_type_id, equip_model_num)
);


