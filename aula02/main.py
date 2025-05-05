from fastapi import FastAPI
from enum import Enum 
from pydantic import BaseModel 
import requests

app = FastAPI()


@app.get("/") #decorador do get relacionado ao endpoint"/""
async def root(): #função assíncrona
    return {"message": "Hello World , Ana!"}

@app.post("/")
async def root():
    return {"message": "post criado!"}

@app.get("/items/{item_id}") #{item_id} é a variavel de rota
async def read_item(item_id : int):
    print("item_id:", item_id)
    print("type(item_id):", type(item_id))
    return {"item_id": item_id}

from enum import Enum 
class BRStates(str, Enum):
    sp = 1
    rj = 2
    mg = 3
    es = 4

@app.get("/states/{state_id}")
async def read_state(state_id: BRStates):
        if state_id.value == "1":
             return {"São Paulo"}
        if state_id.value == "2":
             return {"Rio de janeiro"}
        if state_id.value == "3":
             return {"Minas Gerais"}
        if state_id.value == "4":
             return {"Espírito Santo"}
        
fake_items_db = [{"item_name": "1"}, 
                 {"item_name": "2"}, 
                 {"item_name": "3"}, 
                 {"item_name": "4"}, 
                 {"item_name": "5"}, 
                 {"item_name": "6"}, 
                 {"item_name": "7"}, 
                 {"item_name": "8"}, 
                 {"item_name": "9"},
                 {"item_name": "10"},]


@app.get("/fake_db/")
async def read_item(skip: int = 0, limit: int = 5   ):
    return fake_items_db[skip : skip + limit]


@app.get("/item_name/")
async def item_name(name: str, age: int | None = None, angry: bool = False):
    if age is not None:
          msg= f"My name is {name} and I am {age} years old!"
          return {"message" : msg}
    if angry is not False:
          msg = f"My name is {name} and I am NOT happy! :("
          return {"message" : msg}
    msg = f"My name is {name} and I am happy!"
    return {"message" : msg}

# aula 03 14/04


from typing import Union
from pydantic import  BaseModel
# o none é para declarar quais não são obrigatorios
class Item(BaseModel):
     name: str
     description : Union[str, None] = None
     price : float
     tax: Union [float, None] = None
# esse post é analogo ao que eu fiz na api livro
@app.post('/items/')
async def create_item(item: Item):
     print(item.model_dump())
     return item

class Curso(BaseModel):
     name: str
     duration : int

#update  
@app.put('curso/{curso_id}')
async def update_curso(curso_id:int, curso: Curso):
     return {"curso_id": curso_id, **curso.model_dump()}

from fastapi import  Query
#ler 
@app.get("/items/")
async def read_items(
     q: Union[str, None] = Query(
          default= None,
          max_length=50,
          min_length= 10,
         pattern="^[^\W\d_]{3}$",   # pattern de 3 caracteres,
         title = "Titulo do item",
         description= "Descrição sobre o item deve ser STR"
     )
):
    results = {"item_id": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results





# AULA 4 28/04

'''@app.get("/items2/")
async def read_items2(q: list[str] | None = Query(default=None,title="Valor de consulta padrão nulo",description=
"estou testando...")):
    query_items = {"q": q}
    return query_items'''

# Validação de consulta e de texto
'''@app.get("/items/")
async def read_items(q:list[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items'''
# ----------------------------------------------------------

# validação numerica: maior que ou igual
# ge ->  maior ou igual
# gt -> maior que
# le -> menor ou igual
# lt ->  menor que 

'''''@app.get("/items2/{item_id}")
async def read_items(*, item_id: int = Path(title="The ID of the item to get", ge=1, le=5), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results'''
# ---------------------------------------------------------------


#  Parametro de consulta com modelo pydantic 
'''class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
'''
# ------------------------------------------------------------------------

# restrinja parametros de consulta extra
'''class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query'''
# --------------------------------------------------------------------------

'''class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results'''
# --------------------------------------------------------


# Vetores singulares noi corpo
'''class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items2/{item_id}")
async def update_item(
    item_id: int, item: Item,   importance: Annotated[int, Body()] = 0
):
    results = {
                "item_id": item_id, 
               "item": item,  
               "importance": importance
            }
    return results'''

# -----------------------------------------------------------------------
# q -> query paremetro

# importe field
''''class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
# APARECE MELHOR NA REDOC DO QUE NA DOCS

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results'''
# --------------------------------------------------

# TIPO SET
'''class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    print(results)
    return results'''
# ----------------------------------------------

# defina um sub-modelo

# dicionario dentro do outro
'''class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results'''

#aula 05 05/05/2025

#Codigo de status de resposta 

@app.post("/items3/", status_code=201)
async def create_item(name: str):
    return {"name": name}