from fastapi import FastAPI
from schemas import Item, fakeDatabase
import requests
from requests.structures import CaseInsensitiveDict
import json
from fastapi import HTTPException

app = FastAPI()


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
    newId = len(fakeDatabase.keys()) + 1 # Give the key of dicionarie and add one more
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
        url = f'https://publica.cnpj.ws/cnpj/{cnpj}'
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()

        dataCompany = data['razao_social']
        dataCNPJ = data['cnpj_raiz']

        
        if 'razao_social' and 'cnpj_raiz' in data:
            newEntry = {dataCompany:dataCNPJ}
            fakeDatabase.update(newEntry)
            return fakeDatabase
            
        else:
            return "Dados ausentes na resposta da API externa"
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Erro na solicitação HTTP para a API externa")
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Erro ao processar a resposta da API externa")


"""
    CNPJs: 
    11878898000111
    00623904000173
    06947283000160
    05720854000166
"""