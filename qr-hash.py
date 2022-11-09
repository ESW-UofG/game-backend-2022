import qrcode
from PIL import Image
import random
import os
from dotenv import load_dotenv

#Loads .env variables
load_dotenv()

# Generate the random hash - used to prevent players from cheating and using the same QR code
hash = random.getrandbits(128)
hash = str("%032x" % hash)

#Get number of points from .env file
points = os.environ.get('POINTS')
if points == None:
    print("There is an issue with the .env file. Please edit the .env configuration file. Ex: POINTS=1.")
    exit()
else:
    #Site the QR code will redirect to + unique hash
    input_data = "https://test.com/" + hash + "/" + points
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('./qr-codes/qrcode.png', quality=95)