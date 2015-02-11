create database pyramiddemo default character set = utf8;
grant all on pyramiddemo.* to sylvain@'%' identified by "********";
CREATE TABLE USER(
                LOGIN VARCHAR(16) PRIMARY KEY,
                PASSWD CHAR(64) NOT NULL -- sha-256 hash
);
INSERT INTO USER(LOGIN, PASSWD)
         VALUES ('sylvain', SHA2('sylvain:********',256)),
                ('sonia', SHA2('sonia:******',256));
