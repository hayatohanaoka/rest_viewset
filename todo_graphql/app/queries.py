import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import ToDo, Column

class ToDoNode(DjangoObjectType):
    class Meta:
        model = ToDo
        interfaces = (graphene.relay.Node,)
        filter_fields = ('title',)
        fields = '__all__'

class ToDoQuery(graphene.ObjectType):
    # 内部でリゾルバを持っているので、定義の必要なし
    todo = graphene.relay.Node.Field(ToDoNode)
    all_todos = DjangoFilterConnectionField(ToDoNode)


class Query(graphene.ObjectType):
    todo_query = graphene.Field(ToDoQuery)

    def resolve_todo_query(root, info):
        return ToDoQuery()
