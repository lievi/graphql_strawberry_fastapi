from typing import Optional

from fastapi import FastAPI
from sqlmodel import (
    SQLModel,
    Field,
    create_engine,
    select,
    Session
)

engine = create_engine('sqlite:///data.db')

class Pessoa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    idade: int

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get('/')
def home():
    return {'hello': 'world'}

@app.get('/pessoa')
def get_pessoa():
    query = select(Pessoa)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()
    return result
