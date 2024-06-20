import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphene import relay

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username')
        interfaces = (relay.Node,)


class CreateUser(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        username = inputs['username']
        password = inputs['password']
        user = User.objects.create_user(username=username, password=password)
        return CreateUser(user=user)


class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return 'hello'


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
