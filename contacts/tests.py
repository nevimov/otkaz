from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import FeedbackRequest
from core.management.commands.filldevdb import create_city


class RequestFeedbackTests(TestCase):
    """
    Test case for contacts.views.RequestFeedback.
    """
    URL = reverse('contacts:request-feedback')

    def test_email(self):
        """Test that the view sends a correct email."""
        samara = create_city('Самара', site_domain='samara.otkaz.ru')
        with self.settings(SITE_ID=samara.site.id):
            self.client.post(
                self.URL,
                {
                    'name': 'Liam Neeson',
                    'email': 'liam@neeson.net',
                    'msg_type': FeedbackRequest.MsgTypes.OTHER,
                    'msg': "I have a very particular set of skills.",
                }
            )

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(
            email.subject,
            '[samara.otkaz.ru] Другое: liam@neeson.net Liam Neeson'
        )
        self.assertEqual(
            email.body,
            'Тип сообщения: Другое\n'
            'Имя: Liam Neeson\n'
            'Эл. почта: liam@neeson.net\n'
            'Сообщение: I have a very particular set of skills.'
        )