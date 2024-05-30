import graphene
from .object_types import QuestionType
from .models import Category, Question
from django.shortcuts import get_object_or_404

class CreateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)  # 操作する DjangoObjectType

    class Arguments:
        """
        必要とするフィールド
        """
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.Int()

    @classmethod
    def mutate(cls, root, info, title, content, category_id):
        """
        作成処理
        """
        category = get_object_or_404(Category, pk=category_id)
        question = Question.objects.create(
            title=title,
            content=content,
            category=category
        )
        return CreateQuestion(question=question)  # 自身と同じクラスのインスタンスを返す


class UpdateQuestion(graphene.Mutation):
    question = graphene.Field(QuestionType)

    class Arguments:
        question_id = graphene.ID()
        title = graphene.String()
        content = graphene.String()

    @classmethod
    def mutate(cls, root, info, question_id, title=None, content=None, category_id=None):
        """
        更新処理
        """
        question = get_object_or_404(Question, id=question_id)
        if title:
            question.title = title
        if content:
            question.content = content
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            question.category = category
        question.save()
        return UpdateQuestion(question=question)


class DeleteQuestion(graphene.Mutation):
    is_deleted = graphene.Boolean()

    class Arguments:
        question_id = graphene.Int()
    
    @classmethod
    def mutate(cls, root, info, question_id):
        """
        削除処理
        """
        question = get_object_or_404(Question, id=question_id)
        if question:
            question.delete()
            return DeleteQuestion(is_deleted=True)
        return DeleteQuestion(is_deleted=False)


class Mutation(graphene.ObjectType):
    """
    各ミューテーションをまとめ上げるクラス
    """
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()
