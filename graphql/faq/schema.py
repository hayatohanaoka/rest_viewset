import graphene

from .queries import Query2
from .object_types import AnswerType, QuestionType
from .mutations import Mutation

schema = graphene.Schema(
    query=Query2,
    mutation=Mutation,
    types=[QuestionType, AnswerType]
)
