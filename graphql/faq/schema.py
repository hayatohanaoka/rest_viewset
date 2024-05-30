import graphene

from .queries import Query2
from .mutations import Mutation

schema = graphene.Schema(query=Query2, mutation=Mutation)
