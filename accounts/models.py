from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import Country, CountryField
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField

from django.contrib.auth.models import (
    Permission as BasePermission,
    User as BaseUser,
    Group as BaseGroup,
)
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
from imagekit.models import ImageSpecField
from django.utils.text import slugify


def user_directory_path(instance, filename):
    return f"users/{instance.username}/images/{filename}"

def avatar_upload_path(instance, filename):
    return f"{instance.__class__.__name__}/{filename}"

class User(AbstractUser):
    date_of_birth = models.DateField(_("day of birth"), blank=True, null=True)


class Avatar(models.Model):
    image = models.ImageField(upload_to="avatars")
    class Meta:
        verbose_name = _("Avatar")
        verbose_name_plural = _("Avatars")

    def __str__(self):
        return f"{self.image}" 


class BaseAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    slug = models.SlugField(null=True, blank=True)
    GENDER_CHOICES = (
        ("", _("Choose gender")),
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Others", _("Others")),
    )

    gender = models.CharField(
        _("gender"), max_length=6, choices=GENDER_CHOICES, blank=True
    )
    avatar = models.ForeignKey(Avatar, on_delete=models.DO_NOTHING)

    # avatar_thumbnail = ImageSpecField(
    #     source="avatar", format="JPEG", options={"quality": 60}
    # )

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        _("phone number"), validators=[phone_regex], max_length=17, blank=True
    )  # Validators should be a list

    language = models.CharField(
        _("language"), max_length=5, choices=settings.LANGUAGES, default="en_US"
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def full_name(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if not self.slug and self.id != 1:
            self.slug = slugify(self.get_full_name())
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Student(BaseAccount):
    grade = models.ForeignKey("courses.Grade", on_delete=models.DO_NOTHING, default=1)


class Teacher(BaseAccount):
    headline = models.CharField(_("headline"), max_length=60, blank=True)
    biography = models.TextField(_("biography"), max_length=500, blank=True)

    website = models.CharField(_("website"), max_length=255, null=True, blank=True)
    facebook_url = models.CharField(
        _("facebook"), max_length=255, null=True, blank=True
    )
    twitter_url = models.CharField(_("twitter"), max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(
        _("linkedin"), max_length=255, null=True, blank=True
    )
    youtube_url = models.CharField(_("youtube"), max_length=255, null=True, blank=True)


class Parent(BaseAccount):
    pass


class Group(BaseGroup):
    class Meta:
        proxy = True


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    company_name = models.CharField(max_length=256, blank=True)
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = PhoneNumberField(blank=True, default="", db_index=True)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.first_name + " " + self.last_name


class Enrollment(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.DO_NOTHING, default=1)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, default=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, default=1)

    STATUS_CHOICES = (
        ("enrolled", "Enrolled"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enrolled")

    grade = models.ForeignKey("courses.Grade", on_delete=models.DO_NOTHING, default=1)
    completed_at = models.DateTimeField(null=True, blank=True)
    drop_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
