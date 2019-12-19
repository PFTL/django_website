import hashlib
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.timezone import now


class People(models.Model):
    """ Basic information of the recipients of the messages. It stores the date joined, email and name. It also
    creates a unique identifier to be used for tracking of openings and clicks.
    """
    joined_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    email_verified = models.DateTimeField(null=True)
    active = models.BooleanField(default=False)
    secret_code = models.CharField(max_length=32, null=True)

    def save(self, *args, **kwargs):
        self.secret_code = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        super(People, self).save(*args, **kwargs)

    def __str__(self):
        if self.name:
            return "{} <{}>".format(self.name, self.email)
        return "<{}>".format(self.email)


class FreeChapter(models.Model):
    date_requested = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField(null=True)
    user = models.ForeignKey(People, on_delete=models.CASCADE)
    ip_request = models.GenericIPAddressField(null=True)
    ip_confirmation = models.GenericIPAddressField(null=True)

    def send_confirmation_mail(self, ip_address):
        context = dict(
            user=self.user,
            activation_link=settings.BASE_URL + '/confirm/' + self.user.secret_code,
        )
        mail_text = render_to_string('emails/free_chapter_request.txt', context=context)
        subject = 'Your Python For The Lab Free Chapter'
        email_from = '{} <{}>'.format(settings.DEFAULT_FROM_NAME, settings.DEFAULT_FROM_EMAIL)
        msg = EmailMultiAlternatives(subject, mail_text, email_from, [self.user.email],
                                     reply_to=[settings.DEFAULT_FROM_EMAIL])
        msg.send()
        self.ip_request = ip_address
        self.save()

    def send_free_chapter(self, ip_address):
        context = dict(
            user=self.user,
        )
        mail_text = render_to_string('emails/free_chapter_send.txt', context=context)
        subject = 'Your Python For The Lab Free Chapter'
        email_from = '{} <{}>'.format(settings.DEFAULT_FROM_NAME, settings.DEFAULT_FROM_EMAIL)
        msg = EmailMultiAlternatives(subject, mail_text, email_from, [self.user.email],
                                     reply_to=[settings.DEFAULT_FROM_EMAIL])
        msg.attach_file(os.path.join(settings.BASE_DIR, 'uploads/sample_chapter.pdf'))

        msg.send()
        self.ip_confirmation = ip_address
        self.date_sent = now()
        self.save()