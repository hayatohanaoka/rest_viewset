import graphene
from graphene_django import DjangoListField

from .models import Category, Question, Answer
from .object_types import AnswerType, CategoryType, QuestionType

class Query(graphene.ObjectType):
    # 自動で一覧取得
    all_questions = DjangoListField(QuestionType)
    all_categories = DjangoListField(CategoryType)
    # resolve_~ でオブジェクトの取得をカスタマイズできる
    all_answers = graphene.List(AnswerType, id=graphene.Int(), content=graphene.String())  # 複数取得
    question = graphene.Field(QuestionType, id=graphene.Int())  # 単一取得
    categories_field_by_name = graphene.Field(CategoryType, name=graphene.String())

    def resolve_categories_field_by_name(root, info, **kwargs):
        return Category.objects.get(**kwargs)
    
    def resolve_question(root, info, **kwargs):
        return Question.objects.get(**kwargs)

    def resolve_all_answers(root, info, **kwargs):
        """
        Answers を返す際の処理
        """
        filters = {}

        id_field_name = 'id'
        if id_field_name in kwargs.keys():
            filters[id_field_name] = kwargs[id_field_name]

        content_field_name = 'content'
        if content_field_name in kwargs.keys():
            filters['content__contains'] = kwargs[content_field_name]
        
        answers = Answer.objects
        if filters:
            return answers.filter(**filters)
        return answers


class Query2(graphene.ObjectType):
    """
    GraphQL のクエリフィールドをまとめるためのクラス
    """
    question_query = graphene.Field(Query)

    def resolve_question_query(parent, info):
        return Query()
