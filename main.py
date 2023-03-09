from fastapi import FastAPI
import os
from configparser import ConfigParser
import time
from dotenv import load_dotenv
import awsManager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
SECRET_KEY = os.getenv('SECRET')

app = FastAPI()

# Define the allowed origins
# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/storeHash/{hash_id}/{key}")
def store_hash(hash_id: str, key: str):
    global SECRET_KEY
    # Stores the hash provided by the QR code generator

    # We need to add a secret to this. Maybe through .env?
    # Basically, we need to add some checking because this could easily be hacked
    # So, we can store the hash only if the secrets match which only
    # Maintainers will have access 2 (Matthew, Ian, Martina)
    # If the secret checks out, then the hash will be stored.
    status = ""

    if (key!=SECRET_KEY):
        status = "Not_Stored"
    else:
        awsManager.insertHashItem(hash_id)
        status = "Stored"
    
    return {"status": status}

@app.post("/validateHash/{hash_id}/{email}/{name}/{points}")
def store_hash(hash_id: str, email: str, name: str, points: int):
    # CHECK HASH BOTO3 GOES HERE
    check_stat = awsManager.checkHash(hash_id)

    print(hash_id)
    status = ""
    # Indicated a pass
    if (check_stat == 0):
        ins_stat = awsManager.insertPlayerItem(points, email, name)
        rem_stat = awsManager.removeHash(hash_id)
        if rem_stat == 0 and ins_stat == 0:
            status = "Success"
        else:
            status = "Failure occurred in a function..."
    else:
        print("Hash does not exsist...")
        status = "Failure"

    return {"status": status}

@app.get("/getScores")
def get_scores():
    # GET SCORES FROM BOTO3
    top_five = awsManager.getPlayerScores()
    # RETURN AS JSON
    return {'top_five': top_five}

