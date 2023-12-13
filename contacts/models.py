from core.models import *
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from django_countries.fields import Country, CountryField


def user_directory_path(instance, filename):
    return f'contacts/{instance.name}/avata/{filename}'

class Group(TranslatableModel, models.Model):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), unique=True, blank=True, max_length=255),
        description=models.TextField(
            _('description'), blank=True),
    )
    
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    company = models.CharField(_('Company Name'), max_length=255, blank=True)
    email = models.EmailField(_('Email'), unique=True, db_index=True)
    phone = PhoneNumberField(_('Phone'), blank=True, default="", db_index=True)
    city = models.CharField(max_length=256, blank=True)
    country = CountryField()
    note = models.TextField(_('Notes'), blank=True)
    avatar = models.ImageField(_('Avatar'),
                               upload_to=user_directory_path, blank=True)

    image_thumbnail = ImageSpecField(
        source='avatar', format='JPEG', options={'quality': 60})
    
    group = models.OneToOneField(Group, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')

    def __str__(self):
        return self.name
    


class ContactForm(TranslatableModel, models.Model):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), unique=True,
                              blank=True, max_length=255),
    )
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Contact Form')
        verbose_name_plural = _('Contact Forms')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Mail(TranslatableModel, models.Model):
    contact_form = models.ForeignKey(
        ContactForm, on_delete=models.DO_NOTHING)

    translations = TranslatedFields(
        mail_to=models.CharField(_('To'), max_length=255),
        mail_from=models.CharField(_('From'), max_length=255),
        subject=models.CharField(_('Subject'), max_length=255),
        additional_headers=models.CharField(
            _('Additional headers'), max_length=255, default=_("Reply-To: ")),
        message_body=RichTextUploadingField(_('Message body'), default=_("<p>From: [your-name] &lt;[your-email]&gt;</p><p>Subject: [your-subject]</p><p>Message Body: [your-message]</p><p>-- This e-mail was sent from a contact form on [_site_title] ([_site_url])</p>")))

    class Meta:
        verbose_name = _('Mail')
        verbose_name_plural = _('Mails')

    def __str__(self):
        return self.subject


class Message(TranslatableModel, models.Model):
    contact_form = models.OneToOneField(
        ContactForm, on_delete=models.DO_NOTHING)

    translations = TranslatedFields(
        mail_sent_ok=models.CharField(_("Sender's message was sent successfully"), max_length=255, default=_(
            "Thank you for your message. It has been sent.")),
        mail_sent_ng=models.CharField(_("Sender's message failed to send"), max_length=255, default=_(
            "There was an error trying to send your message. Please try again later.")),
        validation_error=models.CharField(_("Validation errors occurred"), max_length=255, default=_(
            "One or more fields have an error. Please check and try again.")),
    )

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
