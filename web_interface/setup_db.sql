--
-- This script will set up the schema, table and web_user for the book database.
-- It is executed automatically in run_webaccess.py when the application is started
-- with docker-compose up and the schema books does not exist.
--

--
-- A) Create the schema
CREATE SCHEMA IF NOT EXISTS books;

SET search_path TO books;


--
-- B) Create the tables

DROP TABLE IF EXISTS Spine CASCADE;

CREATE TABLE Spine (
    bookID                int                   GENERATED ALWAYS AS IDENTITY,   
    isbn                  varchar(13)           NOT NULL,
    author                varchar(50)           NOT NULL,
    title                 varchar(100)          NOT NULL,
    summary               text                  NOT NULL,
    cover_url             varchar(200)          NOT NULL,
    dt_created            timestamp             NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_modified           timestamp             NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bookID, isbn),
    UNIQUE (bookID),
    UNIQUE (isbn)
);


--
-- C) Create user for connection from web interface

DROP USER IF EXISTS web_user;

CREATE ROLE web_user WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    ENCRYPTED PASSWORD '1234';

GRANT USAGE ON SCHEMA books TO web_user;

GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA books TO web_user;


