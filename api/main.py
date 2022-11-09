from fastapi import FastAPI
import psycopg2
from dotenv import load_dotenv
import os

#Loads .env variables
load_dotenv()

app = FastAPI()
conn = psycopg2.connect(database=os.environ.get('DBNAME'),
                        host=os.environ.get('HOST'),
                        user=os.environ.get('USER_PSQL'),
                        password=os.environ.get('PASSWORD'),
                        port=os.environ.get('PORT'))

cursor = conn.cursor()
print(cursor.execute("SELECT * FROM players"))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/hash/{item_id}")
def store_hash(item_id: int):
     # Stores the hash provided by the QR code generator

    return {"item_id": item_id}
