-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS match;
DROP TABLE IF EXISTS playerStandings;

CREATE DATABASE tournament;
\c tournament;


CREATE TABLE player (
  id serial PRIMARY KEY, 
  playername varchar(50) UNIQUE NOT NULL,
  dateCreated timestamp DEFAULT current_timestamp
);


CREATE TABLE playerStandings (
  id serial PRIMARY KEY, 
  playername varchar(50) UNIQUE NOT NULL,
  wins integer,
  matches integer
);

CREATE TABLE match (
  winner varchar(50) UNIQUE NOT NULL,
  loser varchar(50) UNIQUE NOT NULL 
);

SET search_path TO showfinder,public;

