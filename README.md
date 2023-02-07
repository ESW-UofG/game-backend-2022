# game-backend-2022 :computer:
Backend repo for the games hosted by ESW in 2022/2023


# Setup :gear:

First, clone the repo and change the current directory to 'game-backend-2022'.

This project needs to run a virtual environment locally. Use the following command to do this:

### Virtual environment creation :toolbox:

```bash
python3 -m venv venv
source venv/bin/activate
```
If you would like to exit the virtual environment, enter the following command:

```bash
deactivate
```

### Installing dependencies :hammer:

To install all the dependencies and setup the database, run the following:

```bash
python3 -m pip install -r requirements.txt
```
:warning: currently no command to setup db... :warning:

# Execution :star:

To run the API, simply use the following command in the project's root:
<code>uvicorn main:app --reload</code>

It is important to note that the database needs to be hooked up to a .env file. You can obtain this file from either:
- Matthew Szurkowski
- Ian McKechnie


# How it works... :screwdriver:

The api, and db folders are used on the server, while all the other files are used for QR code generation and sending messages to the server.

The idea is that we will put the QR code generation software on each raspberry pi, the pi once triggered will call the QR code script, generate a QR code, and send a generated HASH to the server. 

The hash generated on QR creation is sent to the server and stored there. When the player scans the QR code, it takes them to the redeem a point page. Built into the URL will be our hash. Redeem a point submission, the hash is sent to the server. If the server verifys that it is a valid hash (verified by being in the hash table) then the player is looked up in another table. If the player is in that table, their score is updated. If they are not in that table, a new account is created for them.
