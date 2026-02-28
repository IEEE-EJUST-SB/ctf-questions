CREATE DATABASE IF NOT EXISTS ctf_lab;
USE ctf_lab;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO users (username, password) VALUES ('flag', 'DEVSTORM{OPPx84$epiIPzPmr}');
INSERT INTO users (username, password) VALUES ('guest', 'guest123');
INSERT INTO users (username, password) VALUES ('admin', 'admin123');
