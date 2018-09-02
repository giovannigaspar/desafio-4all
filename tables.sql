CREATE TABLE RESULTADOS (
    ID          INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    LATITUDE    VARCHAR(25),
    LONGITUDE   VARCHAR(25),
    RUA         VARCHAR(120),
    NUMERO      SMALLINT,
    BAIRRO      VARCHAR(50),
    CIDADE      VARCHAR(70),
    CEP         VARCHAR(20),
    ESTADO      VARCHAR(2),
    PAIS        VARCHAR(60),
    ENDERECO    VARCHAR(300)
);