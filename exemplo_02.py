from typing import Optional

import strawberry

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


@strawberry.type
class Pessoinha:
    id: Optional[int]
    nome: str
    idade: int


@strawberry.type
class Query:
    @strawberry.field
    def all_pessoa(self) -> list[Pessoinha]:
        query = select(Pessoa)
        with Session(engine) as session:
            result = session.execute(query).scalars().all()
        return result

def create_app(idade: int, nome: str):
    person = Pessoa(nome=nome, idade=idade)

    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)

    return person

@strawberry.type
class Mutation:
    create_pessoa: Pessoinha = strawberry.field(
        resolver=create_app
    )


schema = strawberry.Schema(
    query=Query, mutation=Mutation
)