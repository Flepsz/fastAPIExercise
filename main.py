from fastapi import FastAPI
from schemas import Item, fakeDatabase
import requests
import uvicorn
from requests.structures import CaseInsensitiveDict
import json
from fastapi import HTTPException

app = FastAPI()

PROXIES = {
	"http": "http://ct67ca:25INDUSTRIAconectada@proxy.br.bosch.com:8080",
	"https": "http://ct67ca:25INDUSTRIAconectada@proxy.br.bosch.com:8080"
}

@app.get("/")
def getItems():
    return fakeDatabase


# Route with parameter
@app.get("/{id}")
def getItemId(id: int):
    return fakeDatabase[id]

#WithOut class
# @app.post("/")
# def addItem(task: str):
#     newId = len(fakeDatabase.keys()) + 1 # Give the key of dicionarie and add one more
#     fakeDatabase[newId] = {'task': task} # Create a new object
#     return fakeDatabase

#With a class
@app.post("/post")
def addItem(item:Item):
    newId = len(fakeDatabase.keys()) + 1 
    fakeDatabase[newId] = {'company': item.company} 
    return fakeDatabase

@app.put("/{id}")
def updateItem(id: int, item:Item):
    fakeDatabase[id]['company'] = item.company 
    return fakeDatabase

@app.delete("/{id}")
def deleteItem(id: int):
    del fakeDatabase[id]
    return fakeDatabase


@app.get("/cnpj/{cnpj}")
def getAPICNPJ(cnpj: str): 
    try:
        # Requisição da API CNPJ
        url = f'https://publica.cnpj.ws/cnpj/{cnpj}'
        response = requests.get(url, proxies=PROXIES)
        response.raise_for_status()
        
        data = response.json()

        # Json da API
        dataCompany = data['razao_social']
        dataCNPJ = data['cnpj_raiz']

        
        if 'razao_social' and 'cnpj_raiz' in data:
            newId = len(fakeDatabase.keys()) + 1 
            fakeDatabase[newId] = {dataCompany:dataCNPJ} 
            return fakeDatabase
            
        else:
            return "Dados ausentes na resposta da API externa"
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro na solicitação HTTP para a API externa")
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a resposta da API externa")
    
@app.get("/lol/{nickname}")
def getAPInickname(nickname: str):
    try:
        token = "RGAPI-c62b7eac-eed1-4a05-9823-1d858e634191"
        region = "br1"
        # Requisição da API CNPJ
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nickname}?api_key={token}'
        response = requests.get(url, proxies=PROXIES)
        response.raise_for_status()
        
        data = response.json()

        puuid = data["puuid"]
        name = data["name"]
        summonerLevel = data["summonerLevel"]

        return data
            
        # else:
        #     return "Dados ausentes na resposta da API externa"
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro na solicitação HTTP para a API externa")
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a resposta da API externa")
    
@app.get("/lol/{nickname}/top-champions/{count}")
def getAPItopchampions(nickname: str, count: str):
    def read_champion_data():
        with open("champions_data.json", "r") as file:
            data = json.load(file)
        return data
    
    try:
        token = "RGAPI-c62b7eac-eed1-4a05-9823-1d858e634191"
        region = "br1"
        url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{nickname}?api_key={token}'
        
        response_summoner = requests.get(url, proxies=PROXIES)
        response_summoner.raise_for_status()
        
        data_summoner = response_summoner.json()
        data_champions = read_champion_data()

        puuid = data_summoner["puuid"]
        name = data_summoner["name"]

        url_top = f"https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={count}&api_key={token}"
        response_top = requests.get(url_top)
        response_top.raise_for_status()
        data_top = response_top.json()

        maestria_with_names = []
        maestria_with_names.append(name)
        for entry in data_top:
            champion_id = str(entry["championId"])
            champion_name = data_champions.get(champion_id, {}).get("name", "Nome não encontrado")
            entry["championName"] = champion_name
            maestria_with_names.append(entry)
        return maestria_with_names
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro na solicitação HTTP para a API externa")
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a resposta da API externa")


    
if __name__ == "__main__":
    uvicorn.run(app, port=7777)

"""
    CNPJs: 
    11878898000111
    00623904000173
    06947283000160
    05720854000166
    07526557000100
    12648266000124
    12648266000124
    09288252000132
"""