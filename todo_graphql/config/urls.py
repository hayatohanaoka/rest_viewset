from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

from app import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema.schema)),
]
