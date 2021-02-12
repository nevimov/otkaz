from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

__all__ = ['CallbackRequest', 'FeedbackRequest']


class BaseContactRequest(models.Model):
    name = models.CharField("Имя", blank=True, max_length=120)
    datetime_created = models.DateTimeField(
        'Дата и время подачи заявки',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ['-datetime_created']
        verbose_name = 'Контактный запрос'
        verbose_name_plural = 'Контактные запросы'


class CallbackRequest(BaseContactRequest):
    phone = PhoneNumberField('Телефон')
    comment = models.TextField('Комментарий', blank=True, max_length=500)

    class Meta(BaseContactRequest.Meta):
        verbose_name = 'Запрос на обратный звонок'
        verbose_name_plural = 'Запросы на обратный звонок'

    def __str__(self):
        return '%s - %s' % (
            self.phone,
            self.datetime_created.strftime("%Y-%m-%d %H:%M:%S.%f")
        )


class FeedbackRequest(BaseContactRequest):

    class MsgTypes(models.TextChoices):
        ADVICE = 'ADV', 'Предложения по улучшению работы сайта'
        BIZ = 'BIZ', 'Вопросы и предложения о сотрудничестве'
        OTHER = 'OTR', 'Другое'

    msg_type = models.CharField(
        'Тип сообщения',
        max_length=3,
        choices=MsgTypes.choices,
    )
    msg = models.TextField('Сообщение', max_length=2500)
    email = models.EmailField('Email')

    class Meta(BaseContactRequest.Meta):
        verbose_name = 'Запрос на обратный Email'
        verbose_name_plural = 'Запросы на обратный Email'

    def __str__(self):
        return '%s - %s' % (
            self.email,
            self.datetime_created.strftime("%Y-%m-%d %H:%M:%S.%f")
        )