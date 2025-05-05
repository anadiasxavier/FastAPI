from fastapi import FastAPI
from enum import Enum 
from pydantic import BaseModel 
import requests

app = FastAPI()

# @app.get('/')
# def hello_world():
#     return "Hello World 1"

# # Query Param (Paginação)
# @app.get('/filter/')
# def hello_world2(skip: int = 0, limit: int = 10):
#     return f"Hello World 2: {skip}, {limit}"

# # Path Param (Filtro)
# @app.get('/{teste_id}')
# def hello_world3(teste_id):
#     return "Hello World 3: "+teste_id


livros= {
    1:{"titulo": "Amor de Redenção", "autor":"Francine Rivers", "categoria":"Romance", "anoPublicacao":"1991" },
    2:{"titulo": "A ponte de Haven", "autor":"Francine Rivers", "categoria":"Romance", "anoPublicacao":"2014" },
    3:{"titulo": "Asas reluzentes", "autor":"Allison Saft", "categoria":"Fantasia", "anoPublicacao":"2025" },
    4:{"titulo": "Tempestade de Ônix", "autor":"Rebecca Yarros", "categoria":"Fantasia", "anoPublicacao":"2025" },
    5:{"titulo": "Assistente do vilão", "autor":"Hannah Nicole Maehrer", "categoria":"Romance", "anoPublicacao":"2024" },
    6:{"titulo": "Era uma vez um coração partido", "autor":"Rebecca Yarros", "categoria":"Romance", "anoPublicacao":"2022" },
}

class Livro(BaseModel):
    titulo: str
    autor: str
    categoria: str
    anoPublicacao: str

#mostrar todos os livros
@app.get("/")
async def root():
    return{"A nossa biblioteca é ": list(livros.values())}

#selecionar apenas um livro na URL / rota
@app.get("/livros/{item_id}")
async def mostrar_Livro(item_id:int):
    if item_id not in livros:
        return {"mensagem": "Esse livro não foi encontrado, tente novamente!"}
    return livros[item_id]

#Aparecer todos os livro / Consulta
class Livros(int, Enum):
    livro1 = 1
    livro2 = 2
    livro3 = 3
    livro4 = 4
    livro5 = 5
    livro6 = 6


@app.get("/livros/{livros_id}")
async def Consultar_livros(livros_id: Livros):
        if livros_id.value == "1":
             return {"Amor de Redenção"}
        if livros_id.value == "2":
             return {"A ponte de Haven"}
        if livros_id.value == "3":
             return {"Asas reluzentes"}
        if livros_id.value == "4":
             return {"Tempestade de Ônix"}
        if livros_id.value == "5":
             return {"Assistente do vilão"}
        if livros_id.value == "6":
             return {"Era uma vez um coração partido"}
        

# Criar livro / POST
#POST
@app.post("/criar")
async def Criar_livros(livro: Livro):
    novoId = max(livros.keys(), default=0) + 1  
    livros[novoId] = livro.model_dump()  
    return {"mensagem":"Livro cadastrado","id": novoId, "dados": livros}

#EXERCICIO 2 / Consumir api
@app.get("/api")
async def consumir_api():
     url = "https://kanye.rest/"

     try:
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()

          return{"sucesso":True, "dados": data}
     except requests.exceptions.HTTPError as errh:
        return {"status": "erro", "mensagem": f"Erro HTTP: {errh}"}
     except requests.exceptions.RequestException as erro:
        return {"status": "erro", "mensagem": f"Erro ao consumir API: {erro}"}

#EXERCICIO 04 28/04

'''* Parâmetros de consulta e validações de texto
* Parâmetros da Rota e Validações Numéricas
* Modelos de Parâmetros de Consulta
* Corpo - Múltiplos parâmetros
* Corpo - Campos
* Corpo - Modelos aninhados'''

