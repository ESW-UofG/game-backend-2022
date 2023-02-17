import qrcode
from PIL import Image
import random
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet


#Loads .env variables
load_dotenv()

points = str(1)

# Generate the random hash - used to prevent players from cheating and using the same QR code
#hash = random.getrandbits(128)
hash = points
#hash = str("%032x" % hash)

key = Fernet.generate_key()
fernet = Fernet(key)
encMessage = fernet.encrypt(hash.encode())


#Get number of points from .env file
if points == None:
    print("There is an issue with the .env file. Please edit the .env configuration file. Ex: POINTS=1.")
    exit()
else:
    #Site the QR code will redirect to + unique hash
    input_data = "http://10.12.133.27:3000/plinko_game/userId:" + str(encMessage) + "/points:" + points
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('./qr-codes/qrcode.png', quality=95)