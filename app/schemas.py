from typing import Optional

import strawberry
from strawberry.fastapi import GraphQLRouter

from .db_funtions import create_pessoas, create_livro, get_pessoas, get_livros


@strawberry.type
class Pessoa:
    id: Optional[int]
    nome: str
    idade: int
    livros: list['Livro']


@strawberry.type
class Livro:
    id: Optional[int]
    titulo: str
    pessoa: Pessoa


@strawberry.type
class Query:
    all_pessoa: list[Pessoa] = strawberry.field(resolver=get_pessoas)
    all_livro: list[Livro] = strawberry.field(resolver=get_livros)


@strawberry.type
class Mutation:
    create_pessoa: Pessoa = strawberry.field(resolver=create_pessoas)
    create_livro: Pessoa = strawberry.field(resolver=create_livro)


schema = strawberry.Schema(query=Query, mutation=Mutation)


graphql_app = GraphQLRouter(schema)
