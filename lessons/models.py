from email.policy import default
from django.db import models
from parler.models import TranslatableModel, TranslationDoesNotExist
from django.utils.translation import gettext_lazy as _
from core.models import *
from sections.models import *
from accounts.models import *
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager, PolymorphicQuerySet
from polymorphic.models import PolymorphicModel


class Lesson(SectionItem):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1, related_name="lesson_created_by")
    updated_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1, related_name="lesson_updated_by")
    
    # title = models.CharField(_("title"), max_length=255)
    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        try:
            return self.title
        except TranslationDoesNotExist:
            return str(self.id)

    def get_section(self):
        return self.lessons.filter().first()

    def get_items(self):
        return self.items.filter().all()


from parler.managers import TranslatableManager, TranslatableQuerySet
from polymorphic.managers import PolymorphicManager
from polymorphic.query import PolymorphicQuerySet


class CustomQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class CustomManager(PolymorphicManager, TranslatableManager):
    queryset_class = CustomQuerySet


class LessonItem(PolymorphicModel):
    title = models.CharField(_("title"), max_length=255)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.DO_NOTHING, related_name="items"
    )
    
    def __str__(self):
        return self.title


class Learn(LessonItem):
    url = models.URLField(blank=True)
    score = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def get_learnscore_by_user(self):
        res = self.learnscore_set.filter().first()
        if res:
            return 1
        return 0

    def get_items(self):
        return self.items.filter().all()

    class Meta:
        verbose_name = _("Learn")
        verbose_name_plural = _("Learns")


class LearnItem(PolymorphicModel):
    learn = models.ForeignKey(Learn, on_delete=models.DO_NOTHING, related_name="items")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("LearnItem")
        verbose_name_plural = _("LearnItems")


class Video(LearnItem):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        return self.title


from quizzes.models import Quiz


class Test(LearnItem):
    title = models.CharField(max_length=255)
    quiz = models.ForeignKey(
        Quiz, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    @property
    def get_incorrect_questions(self):
        return [int(q) for q in self.incorrect_questions.split(',') if q]
    
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")


class Transcript(TranslatableModel, BaseModel):
    translations = translations()
    time = models.TimeField()
    learn = models.ForeignKey(
        Learn, on_delete=models.DO_NOTHING, related_name="learn_transcripts"
    )

    class Meta:
        verbose_name = _("Transcript")
        verbose_name_plural = _("Transcripts")


# from quizzes.models import *


# class Practice(LessonItem):
#     score = models.IntegerField(default=1)

#     class Meta:
#         verbose_name = _("Practice")
#         verbose_name_plural = _("Practices")

#     def get_questions(self):
#         return self.practice_questions.filter().all()


# class PracticeQuestion(models.Model):
#     practice = models.ForeignKey(
#         Practice,
#         on_delete=models.DO_NOTHING,
#         default=1,
#         related_name="practice_questions",
#     )
#     # question = models.ForeignKey(Question, on_delete=models.DO_NOTHING, default=1)
#     status = models.BooleanField(default=True)
#     position = models.IntegerField(default=0)

#     class Meta:
#         verbose_name = _("Practice Question")
#         verbose_name_plural = _("Practice Questions")

#     def __str__(self):
#         return f"{self.pk}"


# class PracticeAnswer(Answer):
#     class Meta:
#         proxy = True
