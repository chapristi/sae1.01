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

SELECT id, name, scoreRiddle AS score
FROM PLAYER ORDER BY score DESC LIMIT 10;

SELECT id, name, scoreTtt AS score
FROM PLAYER ORDER BY score DESC LIMIT 10;

SELECT id, name,scoreMatches AS score
FROM PLAYER ORDER BY score DESC LIMIT 10;

SELECT id, name, scoreP4 AS score
FROM PLAYER ORDER BY score DESC LIMIT 10;


