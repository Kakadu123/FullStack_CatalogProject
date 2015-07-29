
### Details to set up the environment:
* Install Vagrant and VirtualBox
* Clone the fullstack-nanodegree-vm repository (navigate to vagrant directory)
* Launch the Vagrant VM ( commands: *vagrant up* and *vagrant ssh*)

[detailed instructions](https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true)

### Instructions to run the application
* Type *psql* to get into Postgres database
* create tournament (*drop database if exists tournament;* and *create database tournament;*), 
* connect to tournament database (*\c tournament*), 
* import database schema including tables and view (*\i tournament.sql*),
* exit psql and run *tournament_test.py* (*python tournament_test.py*) to check compliance with all tests

Database schema including Tables and Views is located in tournament.sql, while code logic is encapsulated in functions located in tournament.py.
