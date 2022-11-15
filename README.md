# game-backend-2022 :computer:
Backend repo for the games hosted by ESW in 2022/2023


# Setup :gear:

Clone the repo, and change the current directory to 'game-backend-2022'.
To install all the dependencies and setup the database, run the install script by using: <code>./install-script </code>

# How it works... :screwdriver:

The api, and db folders are used on the server, while all the other files are used for QR code generation and sending messages to the server.

The idea is that we will put the QR code generation software on each raspberry pi, the pi once triggered will call the QR code script, generate a QR code, and send a generated HASH to the server. 

The hash generated on QR creation is sent to the server and stored there. When the player scans the QR code, it takes them to the redeem a point page. Built into the URL will be our hash. Redeem a point submission, the hash is sent to the server. If the server verifys that it is a valid hash (verified by being in the hash table) then the player is looked up in another table. If the player is in that table, their score is updated. If they are not in that table, a new account is created for them.
