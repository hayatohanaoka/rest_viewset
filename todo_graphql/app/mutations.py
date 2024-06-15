import graphene
from django.shortcuts import get_object_or_404
from graphql_relay.node import node

from .models import Column
from .queries import ColumnNode

class CreateColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    column = graphene.Field(ColumnNode)  # 返り値を格納するためのフィールド

    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        title = inputs['title']
        description = inputs['description']
        column = Column.objects.create(
            title=title, description=description, user_id=1)
        
        return CreateColumnMutation(column=column)


class UpdateColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        column_id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    column = graphene.Field(ColumnNode)  # 返り値を格納するためのフィールド

    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        column_id   = inputs['column_id']
        title       = inputs['title'] if 'title' in inputs.keys() else None
        description = inputs['description'] if 'description' in inputs.keys() else None

        _, model_id = node.from_global_id(column_id)
        column = get_object_or_404(Column, pk=model_id)

        if title is not None:
            column.title = title
        if description is not None:
            column.description = description
        
        column.save()

        return UpdateColumnMutation(column=column)


class DeleteColumnMutation(graphene.relay.ClientIDMutation):
    class Input:
        column_id = graphene.ID(required=True)

    ok = graphene.Boolean()  # 返り値を格納するためのフィールド

    @classmethod
    def mutate_and_get_payload(cls, root, info, **inputs):
        column_id = inputs['column_id']
        _, model_id = node.from_global_id(column_id)
        column = get_object_or_404(Column, pk=model_id)
        column.delete()

        return DeleteColumnMutation(ok=True)


class Mutation(graphene.ObjectType):
    create_column = CreateColumnMutation.Field()
    update_column = UpdateColumnMutation.Field()
    delete_column = DeleteColumnMutation.Field()
