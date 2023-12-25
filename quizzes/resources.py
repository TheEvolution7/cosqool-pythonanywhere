from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Quiz, Question, Answer


class QuestionResource(resources.ModelResource):
    quiz = fields.Field(
        column_name="quiz",
        attribute="quiz",
        widget=ForeignKeyWidget(Quiz, field="title"),
    )

    # answers = fields.Field(
    #     column_name="answers",
    #     attribute="answers",
    #     widget=ManyToManyWidget(Answer, field="content", separator="|"),
    # )

    class Meta:
        model = Question
