CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    idade INT,
    sexo VARCHAR(10),
    id_mongo_certificado VARCHAR(50),
    localizacao VARCHAR(255)
);


