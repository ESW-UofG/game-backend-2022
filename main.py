from fastapi import FastAPI
import os
from configparser import ConfigParser
import time

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/hash/{hash_id}/{email}/{name}/{points}")
def store_hash(hash_id: str, email: str, name: str, points: int):
    # Stores the hash provided by the QR code generator

    # CHECK HASH BOTO3 GOES HERE

    # UPDATE PLAYER TABLE
    print(hash_id)
    return {"hash_id": hash_id, "email": email, "name": name, "points": points }

@app.get("/getScores")
def get_scores():
    # GET SCORES FROM BOTO3

    # RETURN THE TOP 5 VALUES (MANIPULATE THE PANDAS DF)

    # RETURN AS JSON
    return {}

