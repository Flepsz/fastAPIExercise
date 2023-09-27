from fastapi import FastAPI
from schemas import Item, fakeDatabase
import requests
import json
from requests.structures import CaseInsensitiveDict

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
@app.post("/")
def addItem(item:Item):
    newId = len(fakeDatabase.keys()) + 1 # Give the key of dicionarie and add one more
    fakeDatabase[newId] = {item.task: item.task} # Create a new object
    return fakeDatabase

# OBS: When the method pass many parameters, its better create a class

@app.put("/{id}")
def updateItem(id: int, item:Item):
    fakeDatabase[id]['task'] = item.task 
    return fakeDatabase

@app.delete("/{id}")
def deleteItem(id: int):
    del fakeDatabase[id]
    return fakeDatabase

@app.get("/cnpj/{cnpj}")
def getAPICNPJ(cnpj: str): 
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 404:
            return "CNPJ não encontrado."
        
        data = response.json()
        
        if 'cnpj_raiz' in data and 'razao_social' in data:
            return data['cnpj_raiz']['razao_social']
        else:
            return "Dados não encontrados na resposta da API."
    
    except requests.exceptions.RequestException as e:
        return f"Erro na solicitação HTTP: {e}"
    
    except ValueError as e:
        return f"Erro na análise JSON: {e}"