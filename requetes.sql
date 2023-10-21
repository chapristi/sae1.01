-- SQLite
CREATE TABLE PLAYER
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) UNIQUE,
    password VARCHAR(150),
    scoreRiddle SMALLINT NOT NULL,
    scoreTtt SMALLINT NOT NULL,
    scoreMatches SMALLINT NOT NULL,
    scoreP4 SMALLINT NOT NULL
)
INSERT INTO PLAYER (name,password,scoreRiddle,scoreTtt,scoreMatches,scoreP4) VALUES ('valeurf', 'valeur2',0,0,0,0)

SELECT * FROM PLAYER WHERE name = 'valeur 5' AND password = 'valeur 2'
SELECT * FROM PLAYER
