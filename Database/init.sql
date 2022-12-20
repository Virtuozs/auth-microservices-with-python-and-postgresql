DO $$
BEGIN
CREATE USER auth1 with encrypted password 'password';
EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, skipping', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON DATABASE auth TO auth1;

\connect auth

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE users TO auth1;

INSERT INTO users (id, email, password) VALUES (DEFAULT, 'test@mail.com', 'password');