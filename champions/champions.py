from fastapi import FastAPI
import requests
import uvicorn
import json
from fastapi import HTTPException

app = FastAPI()

def read_champion_data():
    with open("champions_data.json", "r") as file:
        data = json.load(file)
    return data

champion_data = read_champion_data()

@app.get("/champion-data")
def get_champion_data():
    return champion_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5555)