
-- lucas 1
-- roy 2

-- INSERT INTO users (id, username, password, name, mobilenumber, email) VALUES
--     --(1, 'lucas', generate_password_hash('123'), "Lucas Blotta", '11996786683', 'lucas@example.com'),
--     (1, 'lucas', 'pbkdf2:sha256:260000$uwQY5aHHumXBsSFz$f00666b32ca196b0a23b85e4bdb34bcda872c972440a4df698712bcc0f591d51'
--         , "Lucas Blotta", '11996786683', 'lucas@example.com'),
--     (2, 'roy', 'pbkdf2:sha256:260000$zjtB7P1ocyyHnXu0$06347f1fcdacb877ce702c795e7c171e1d1f8d78115162cee291636eb5e62373'
--         , "Roy Raynalds", '11996786684', 'roy@example.com');

-- lucas Colaborador
INSERT INTO user_roles (user_id, role_id) VALUES (1, 0);

INSERT INTO addresses (user_id, zipcode, street, number, complement, city, state, active) VALUES
    (2, '05652000', 'Av Roberto Marinho', 5219, 'C3', 'São Paulo', 'SP', 1);

INSERT INTO beneficiarios (id, responsavel_id, name, dataNascimento, altura, peso, nrCalcado, active) VALUES
    (1, 2, "Maria Gonçalves", '1998-11-30 00:00:00', 1.70, 68, NULL, 1);