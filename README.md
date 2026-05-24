# Password-Manager
A password manager that I'm building from scratch. I'm utilizing Python and the hashlib libraries, specifcally scrypt, as well as SQLite to keep track of the passwords in a database

## Task list of things to do
    - [x] Start writing the HashingUtils.py file
    - [x] Do research on password managers and how they work
    - [x] Complete the key generation and verification steps in HashingUtils that will be used to allow you to login
    - [ ] ~~Create a structure for the HashingUtils python script that allows for public and private functions to keep things organized~~ This step was kind of useless, it was a lot better in theory, but what is more important is the proper handling of overwriting and releasing data from memory
    - [ ] Figure out and understand exactly when and where the passwords should be hashed or encrypted, and how the client end works in a password manager
    - [ ] Create a database and play around with one to remind myself of my SQL skills and how to properly setup the database to my needs
    - [ ] Research about how to make python scripts to interact with the database directly like querying and entering data
    - [ ] Start a document that shows the structure of the project to keep myself logically sound and accurate in my implementation
    - [ ] Build the small application with visuals that allows me to login with a username and password to access my section of the database

## 5/22/2026
    - Created a general basis for the project by starting to understand the hashlib library and playing around with some of the functions
    - Edited the README and started to create a general task list to keep myself on track in this README

## 5/23/2026
    - I found that hashlib does not support a context field which is important for creating the encryption and verification keys for the master password that is created for each account
    - I have found the the HKDF function in the cryptography library of python will work well for deriving multiple keys in different context fields
    - I have successfully implemented the keyDerivation function correctly and confirmed that verifyPW will output the same exact encryption key after verifying that the derived verification key is also the same
    - The biggest hurdle I believe is over, I now have to build the structure for the encryption schemes within the database and learn exactly how to use the sqlite library to interact with a database that I create

## 5/24/2026
    - Created a solid setup for the tables in my database
    - Played around with some of the other libraries I need to use for this project. I've found that today has been a lot slower than the other few days, but I believe today was a good learning day for me.
    - Improved upon HashingUtils.py, I was returning some stuff that was unnecessary in key derivation. It was good for testing, but returning the encryption key when deriving the keys is unnecessary when it gets derived every time you verify the password that was input is correct.
    - 