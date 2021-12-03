from sqlmodel import Session, select
from sqlalchemy.orm import joinedload

from .models import Pessoa, Livro, engine


def create_pessoas(idade: int, nome: str):
    person = Pessoa(nome=nome, idade=idade)

    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)

    return person


def create_livro(titulo: str, pessoa_id: int):
    livro = Livro(titulo=titulo, pessoa_id=pessoa_id)

    with Session(engine) as session:
        session.add(livro)
        session.commit()
        session.refresh(livro)

    return livro


def get_pessoas():
    query = select(Pessoa)

    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result

def get_pessoa(
    id: int = None,
    idade: int = None,
    limit: int = 2
):
    query = select(Pessoa)

    with Session(engine) as session:
        result = session.execute(query).scalars().all()

    return result


def get_livros():
    # Este joinedload "força" o select das relações, nesse caso, a pessoa
    query = select(Livro).options(joinedload('pessoa'))

    with Session(engine) as session:
        result = session.execute(query).scalars().unique().all()

    return result