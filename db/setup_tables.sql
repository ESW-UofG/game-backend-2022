CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    email TEXT,
    username TEXT,
    points INT DEFAULT 0
); 

CREATE TABLE hashes (
    qr_hash TEXT NOT NULL
);