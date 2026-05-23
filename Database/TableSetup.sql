/* The current table being created, VerificationKey is only 48 bytes for a reason
16 bytes of salt + the 32 bytes for the key*/
CREATE TABLE master (VerificationKey VARCHAR(48) PRIMARY KEY, Username CHAR(255));

/* Example of an insert into statement for the table*/
INSERT INTO master (VerificationKey, Username) VALUES (78497321984312, "BiggusDickus");

/* This should be ran on the master table to ensure that only one user can exist
    The implementation is simply for one user, me*/
CREATE UNIQUE INDEX one_row_only_uidx ON master ((true));

/* Use this after messing around with the table. I want to make the table with
my python script*/
DROP TABLE master;