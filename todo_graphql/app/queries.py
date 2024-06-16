from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node import node
from django.core.exceptions import ObjectDoesNotExist

from .models import ToDo, Column

class ToDoNode(DjangoObjectType):
    class Meta:
        model = ToDo
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'priority': ['exact', 'lt', 'gt', 'lte', 'gte']
        }
        fields = '__all__'


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.Node,)


class ColumnNode(DjangoObjectType):
    class Meta:
        model = Column
        interfaces = (graphene.Node,)
        filter_fields = ('title',)
        fields = '__all__'


class OrderByEnum(graphene.Enum):
    TITLE_ASC = 'title'
    TITLE_DESC = '-title'
    PRIORITY_ASC = 'priority'
    PRIORITY_DESC = '-priority'


class ToDoQuery(graphene.ObjectType):
    # 内部でリゾルバを持っているので、定義の必要なし
    todo = graphene.relay.Node.Field(ToDoNode)
    all_todos = DjangoFilterConnectionField(ToDoNode, orderBy=graphene.List(of_type=OrderByEnum))
    todo_by_global_id = graphene.Field(ToDoNode, global_id=graphene.ID(required=True))

    def resolve_all_todos(root, info, **kwargs):
        query_set = ToDo.objects.all()
        if 'orderBy' in kwargs:
            # OrderByEnumクラスの各プロパティの値を取得する
            order_by_fields = [command.value for command in kwargs['orderBy']]
            query_set = query_set.order_by(*order_by_fields)
        return query_set

    def resolve_todo_by_global_id(root, info, global_id):
        try:
            # _type: str Nodeのタイプ, _id: str NodeのグローバルID
            _type, _id = node.from_global_id(global_id)
            print(_type, _id)
            return ToDo.objects.get(id=_id)
        except ObjectDoesNotExist:
            return None



class ColumnQuery(graphene.ObjectType):
    column = graphene.relay.Node.Field(ColumnNode)
    all_columns = DjangoFilterConnectionField(ColumnNode)


class Query(graphene.ObjectType):
    todo_query = graphene.Field(ToDoQuery)
    column_query = graphene.Field(ColumnQuery)
    node = graphene.relay.Node.Field()  # Node全体を扱う

    def resolve_todo_query(root, info):
        return ToDoQuery()
    
    def resolve_column_query(root, info):
        return ColumnQuery()
