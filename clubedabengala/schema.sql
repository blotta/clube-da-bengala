
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS beneficiarios;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

DROP TABLE IF EXISTS emprestimos_status;
DROP TABLE IF EXISTS emprestimos;
DROP TABLE IF EXISTS solicitacoes;

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


-- CREATE TABLE solicitacoes (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   status INTEGER NOT NULL,
--   solicitante_id INTEGER NOT NULL,

--   FOREIGN KEY (solicitante_id) REFERENCES users (id)
-- );


CREATE TABLE emprestimos_status (
  id INTEGER PRIMARY KEY,
  status TEXT UNIQUE NOT NULL
);

INSERT INTO emprestimos_status (id, status) VALUES
    (0, 'Solicitado')
  , (1, 'Aprovado')
  , (2, 'Negado')
  , (3, 'Emprestado');

CREATE TABLE emprestimos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- solicitacao_id INTEGER NOT NULL,
  status INTEGER NOT NULL,
  solicitante_id INTEGER NOT NULL,
  beneficiario_id INTEGER NOT NULL,

  -- FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes (id),
  FOREIGN KEY (solicitante_id) REFERENCES users (id),
  FOREIGN KEY (beneficiario_id) REFERENCES beneficiarios (id),
  FOREIGN KEY (status) REFERENCES emprestimos_status (id)
);


