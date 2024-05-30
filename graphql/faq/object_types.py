from graphene_django import DjangoObjectType

from .models import Category, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = '__all__'

    @classmethod
    def get_queryset(cls, queryset, info):
        origin_queryset = super().get_queryset(queryset, info)
        # return origin_queryset.filter(is_published=True)
        return origin_queryset.filter()


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        exclude = ('created_at',)